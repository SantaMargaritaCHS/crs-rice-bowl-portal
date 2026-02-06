"""Seed script to add missing theology classes."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, SchoolClass

NEW_CLASSES = [
    # Ms. Hawks - missing Period 4
    "Ms. Hawks' Period 4",

    # Mr. Peck - all teaching periods
    "Mr. Peck's Period 1",
    "Mr. Peck's Period 2",
    "Mr. Peck's Period 3",
    "Mr. Peck's Period 4",
    "Mr. Peck's Period 6",
    "Mr. Peck's Period 7",

    # Mrs. Poyar - teaching periods (not Campus Ministry)
    "Mrs. Poyar's Period 1",
    "Mrs. Poyar's Period 4",
    "Mrs. Poyar's Period 5",
    "Mrs. Poyar's Period 6",

    # Mr. Robison - teaching periods (not Prep/Service)
    "Mr. Robison's Period 2",
    "Mr. Robison's Period 3",
    "Mr. Robison's Period 4",
    "Mr. Robison's Period 5",
    "Mr. Robison's Period 7",

    # Mr. Schanzenbach - teaching periods (not Prep/Service)
    "Mr. Schanzenbach's Period 1",
    "Mr. Schanzenbach's Period 2",
    "Mr. Schanzenbach's Period 5",
    "Mr. Schanzenbach's Period 6",
    "Mr. Schanzenbach's Period 7",

    # Mr. Swoboda - teaching periods (not Prep/Service)
    "Mr. Swoboda's Period 1",
    "Mr. Swoboda's Period 2",
    "Mr. Swoboda's Period 4",
    "Mr. Swoboda's Period 5",
    "Mr. Swoboda's Period 6",

    # Mrs. Townsend - teaching periods (not Prep/Service)
    "Mrs. Townsend's Period 2",
    "Mrs. Townsend's Period 3",
    "Mrs. Townsend's Period 4",
    "Mrs. Townsend's Period 5",
    "Mrs. Townsend's Period 7",

    # Mr. VanderWilt - teaching periods (not Prep/Service)
    "Mr. VanderWilt's Period 1",
    "Mr. VanderWilt's Period 3",
    "Mr. VanderWilt's Period 4",
    "Mr. VanderWilt's Period 6",
    "Mr. VanderWilt's Period 7",

    # Mr. Visconti - only Period 2 (rest are Campus Ministry)
    "Mr. Visconti's Period 2",
]


def seed():
    """Add missing theology classes to the database."""
    app = create_app()
    with app.app_context():
        print(f"\n[SEED] Starting seed operation...")
        print(f"[SEED] Adding {len(NEW_CLASSES)} classes...\n")

        added = 0
        skipped = 0

        for name in NEW_CLASSES:
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


if __name__ == '__main__':
    seed()
