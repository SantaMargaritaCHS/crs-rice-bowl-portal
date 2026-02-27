"""
Application entry point for the CRS Rice Bowl application.
"""
import os
import sys
import threading
import urllib.request

# Startup logging for Railway debugging
print(f"[STARTUP] Python version: {sys.version}", flush=True)
print(f"[STARTUP] PORT env: {os.environ.get('PORT', 'not set')}", flush=True)
print(f"[STARTUP] Working dir: {os.getcwd()}", flush=True)

from app import create_app

print(f"[STARTUP] DATABASE_URL set: {'yes' if os.environ.get('DATABASE_URL') else 'NO - will use SQLite!'}", flush=True)
db_url = os.environ.get('DATABASE_URL', '')
if db_url:
    # Show host portion only (mask credentials)
    at_idx = db_url.find('@')
    if at_idx > 0:
        print(f"[STARTUP] DB host: {db_url[at_idx+1:]}", flush=True)

print("[STARTUP] Creating Flask app...", flush=True)
app = create_app()
print("[STARTUP] Flask app created successfully!", flush=True)

# Log database state and run migrations
with app.app_context():
    from app.models import SchoolClass, Quiz, Setting, Announcement, db
    from sqlalchemy import text, inspect

    print(f"[STARTUP] Actual DB URI: {app.config['SQLALCHEMY_DATABASE_URI'][:60]}...", flush=True)

    # One-time migration: add cash_amount column to school_classes
    # MUST run before any SchoolClass ORM queries (model includes cash_amount)
    if not Setting.get('cash_amount_migration_done'):
        print("[STARTUP] Running cash_amount column migration...", flush=True)
        try:
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('school_classes')]
            if 'cash_amount' not in columns:
                db.session.execute(text('ALTER TABLE school_classes ADD COLUMN cash_amount FLOAT NOT NULL DEFAULT 0.0'))
                db.session.commit()
                print("[STARTUP] Added cash_amount column to school_classes", flush=True)
            else:
                print("[STARTUP] cash_amount column already exists", flush=True)
            Setting.set('cash_amount_migration_done', 'true')
        except Exception as e:
            print(f"[STARTUP] cash_amount migration failed: {e}", flush=True)
            db.session.rollback()

    class_count = SchoolClass.query.count()
    quiz_count = Quiz.query.count()
    print(f"[STARTUP] Classes in DB: {class_count}", flush=True)
    print(f"[STARTUP] Quizzes in DB: {quiz_count}", flush=True)

    # Auto-seed classes if database is empty
    if class_count == 0:
        print("[STARTUP] No classes found - running auto-seed...", flush=True)
        try:
            from seed_classes import ALL_CLASSES
            added = 0
            for name in ALL_CLASSES:
                existing = SchoolClass.query.filter_by(name=name).first()
                if not existing:
                    new_class = SchoolClass(name=name, rice_bowl_amount=0.0)
                    db.session.add(new_class)
                    added += 1
            db.session.commit()
            print(f"[STARTUP] Auto-seeded {added} classes!", flush=True)
        except Exception as e:
            print(f"[STARTUP] Auto-seed failed: {e}", flush=True)
            db.session.rollback()

    # One-time migration: convert existing quiz/announcement datetimes
    # from Pacific Time (stored naively) to proper UTC.
    if not Setting.get('tz_migration_done'):
        print("[STARTUP] Running timezone migration (PT -> UTC)...", flush=True)
        try:
            from zoneinfo import ZoneInfo
            PACIFIC = ZoneInfo('America/Los_Angeles')
            UTC = ZoneInfo('UTC')

            migrated = 0
            for quiz in Quiz.query.all():
                changed = False
                if quiz.opens_at:
                    aware_pt = quiz.opens_at.replace(tzinfo=PACIFIC)
                    quiz.opens_at = aware_pt.astimezone(UTC).replace(tzinfo=None)
                    changed = True
                if quiz.closes_at:
                    aware_pt = quiz.closes_at.replace(tzinfo=PACIFIC)
                    quiz.closes_at = aware_pt.astimezone(UTC).replace(tzinfo=None)
                    changed = True
                if changed:
                    migrated += 1

            for ann in Announcement.query.all():
                changed = False
                if ann.start_at:
                    aware_pt = ann.start_at.replace(tzinfo=PACIFIC)
                    ann.start_at = aware_pt.astimezone(UTC).replace(tzinfo=None)
                    changed = True
                if ann.end_at:
                    aware_pt = ann.end_at.replace(tzinfo=PACIFIC)
                    ann.end_at = aware_pt.astimezone(UTC).replace(tzinfo=None)
                    changed = True
                if changed:
                    migrated += 1

            Setting.set('tz_migration_done', 'true')
            db.session.commit()
            print(f"[STARTUP] Timezone migration complete: {migrated} records updated", flush=True)
        except Exception as e:
            print(f"[STARTUP] Timezone migration failed: {e}", flush=True)
            db.session.rollback()

# Keep-alive self-ping to prevent Railway from idling the service.
# This ensures scheduled quizzes go live at the right time.
def _keep_alive():
    """Ping our own health endpoint every 10 minutes to prevent idle shutdown."""
    port = os.environ.get('PORT', '5000')
    url = f'http://localhost:{port}/api/health'
    try:
        urllib.request.urlopen(url, timeout=10)
    except Exception:
        pass  # Server might not be ready yet; that's fine
    # Schedule next ping
    timer = threading.Timer(600, _keep_alive)  # 10 minutes
    timer.daemon = True
    timer.start()

# Start keep-alive after a 30-second delay (let gunicorn boot first)
_startup_timer = threading.Timer(30, _keep_alive)
_startup_timer.daemon = True
_startup_timer.start()
print("[STARTUP] Keep-alive self-ping scheduled (every 10 minutes)", flush=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[STARTUP] Starting development server on port {port}", flush=True)
    app.run(debug=True, host='0.0.0.0', port=port)
