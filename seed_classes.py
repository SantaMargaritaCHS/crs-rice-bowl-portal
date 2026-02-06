"""Seed script to add all theology classes."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, SchoolClass

ALL_CLASSES = [
    # === ORIGINAL CLASSES (were in the database before) ===

    # Mr. Bilash - Periods 1, 2, 3, 4, 6, 7
    "Mr. Bilash's Period 1",
    "Mr. Bilash's Period 2",
    "Mr. Bilash's Period 3",
    "Mr. Bilash's Period 4",
    "Mr. Bilash's Period 6",
    "Mr. Bilash's Period 7",

    # Mr. DeVera - Periods 2, 3
    "Mr. DeVera's Period 2",
    "Mr. DeVera's Period 3",

    # Mr. Dimler - Periods 1, 2, 3, 4, 6
    "Mr. Dimler's Period 1",
    "Mr. Dimler's Period 2",
    "Mr. Dimler's Period 3",
    "Mr. Dimler's Period 4",
    "Mr. Dimler's Period 6",

    # Mr. Ledezma - Period 7
    "Mr. Ledezma's Period 7",

    # Mr. Omlin - Periods 2, 3, 4, 5, 6, 7
    "Mr. Omlin's Period 2",
    "Mr. Omlin's Period 3",
    "Mr. Omlin's Period 4",
    "Mr. Omlin's Period 5",
    "Mr. Omlin's Period 6",
    "Mr. Omlin's Period 7",

    # Ms. Hawks - Periods 2, 6, 7
    "Ms. Hawks' Period 2",
    "Ms. Hawks' Period 6",
    "Ms. Hawks' Period 7",

    # Ms. Martinez - Periods 2, 3, 4, 5, 6
    "Ms. Martinez's Period 2",
    "Ms. Martinez's Period 3",
    "Ms. Martinez's Period 4",
    "Ms. Martinez's Period 5",
    "Ms. Martinez's Period 6",

    # Ms. Moreno - Periods 1, 3, 4, 5, 7
    "Ms. Moreno's Period 1",
    "Ms. Moreno's Period 3",
    "Ms. Moreno's Period 4",
    "Ms. Moreno's Period 5",
    "Ms. Moreno's Period 7",

    # Ms. Nunes - Periods 2, 3, 5, 7
    "Ms. Nunes' Period 2",
    "Ms. Nunes' Period 3",
    "Ms. Nunes' Period 5",
    "Ms. Nunes' Period 7",

    # === NEW CLASSES (from Theology schedule) ===

    # Ms. Hawks - missing Period 4
    "Ms. Hawks' Period 4",

    # Mr. Peck - Periods 1, 2, 3, 4, 6, 7
    "Mr. Peck's Period 1",
    "Mr. Peck's Period 2",
    "Mr. Peck's Period 3",
    "Mr. Peck's Period 4",
    "Mr. Peck's Period 6",
    "Mr. Peck's Period 7",

    # Mrs. Poyar - Periods 1, 4, 5, 6
    "Mrs. Poyar's Period 1",
    "Mrs. Poyar's Period 4",
    "Mrs. Poyar's Period 5",
    "Mrs. Poyar's Period 6",

    # Mr. Robison - Periods 2, 3, 4, 5, 7
    "Mr. Robison's Period 2",
    "Mr. Robison's Period 3",
    "Mr. Robison's Period 4",
    "Mr. Robison's Period 5",
    "Mr. Robison's Period 7",

    # Mr. Schanzenbach - Periods 1, 2, 5, 6, 7
    "Mr. Schanzenbach's Period 1",
    "Mr. Schanzenbach's Period 2",
    "Mr. Schanzenbach's Period 5",
    "Mr. Schanzenbach's Period 6",
    "Mr. Schanzenbach's Period 7",

    # Mr. Swoboda - Periods 1, 2, 4, 5, 6
    "Mr. Swoboda's Period 1",
    "Mr. Swoboda's Period 2",
    "Mr. Swoboda's Period 4",
    "Mr. Swoboda's Period 5",
    "Mr. Swoboda's Period 6",

    # Mrs. Townsend - Periods 2, 3, 4, 5, 7
    "Mrs. Townsend's Period 2",
    "Mrs. Townsend's Period 3",
    "Mrs. Townsend's Period 4",
    "Mrs. Townsend's Period 5",
    "Mrs. Townsend's Period 7",

    # Mr. VanderWilt - Periods 1, 3, 4, 6, 7
    "Mr. VanderWilt's Period 1",
    "Mr. VanderWilt's Period 3",
    "Mr. VanderWilt's Period 4",
    "Mr. VanderWilt's Period 6",
    "Mr. VanderWilt's Period 7",

    # Mr. Visconti - Period 2
    "Mr. Visconti's Period 2",
]


def seed():
    """Add all theology classes to the database."""
    app = create_app()
    with app.app_context():
        print(f"\n[SEED] Starting seed operation...")
        print(f"[SEED] Adding {len(ALL_CLASSES)} classes...\n")

        added = 0
        skipped = 0

        for name in ALL_CLASSES:
            existing = SchoolClass.query.filter_by(name=name).first()
            if existing:
                print(f"  SKIP (exists): {name}")
                skipped += 1
            else:
                new_class = SchoolClass(name=name, rice_bowl_amount=0.0)
                db.session.add(new_class)
                print(f"  ADDED: {name}")
                added += 1

        db.session.commit()
        print(f"\n[SEED] Done! Added {added} classes, skipped {skipped} existing.")
        print(f"[SEED] Total classes in database: {SchoolClass.query.count()}")


if __name__ == '__main__':
    seed()
