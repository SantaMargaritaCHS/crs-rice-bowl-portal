"""
Application entry point for the CRS Rice Bowl application.
"""
import os
import sys

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

# Log database state
with app.app_context():
    from app.models import SchoolClass, Quiz, db
    class_count = SchoolClass.query.count()
    quiz_count = Quiz.query.count()
    print(f"[STARTUP] Classes in DB: {class_count}", flush=True)
    print(f"[STARTUP] Quizzes in DB: {quiz_count}", flush=True)
    print(f"[STARTUP] Actual DB URI: {app.config['SQLALCHEMY_DATABASE_URI'][:60]}...", flush=True)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[STARTUP] Starting development server on port {port}", flush=True)
    app.run(debug=True, host='0.0.0.0', port=port)
