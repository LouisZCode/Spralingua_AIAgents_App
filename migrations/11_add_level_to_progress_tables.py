"""
Migration to add level field to exercise_progress and topic_progress tables.
This enables tracking progress independently for each level (A1, A2, B1, B2).

Run this migration with: uv run python migrations/11_add_level_to_progress_tables.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text
import traceback

def run_migration():
    """Add level field to progress tracking tables"""

    with app.app_context():
        try:
            print("\n" + "="*50)
            print("Starting Migration: Add Level to Progress Tables")
            print("="*50)

            # Step 1: Clear existing data (fresh start as discussed)
            print("\n[Step 1/5] Clearing existing progress data (fresh start)...")
            db.session.execute(text("DELETE FROM exercise_progress"))
            db.session.execute(text("DELETE FROM topic_progress"))
            db.session.commit()
            print("[SUCCESS] Cleared existing progress data")

            # Step 2: Add level column to exercise_progress
            print("\n[Step 2/5] Adding level column to exercise_progress table...")
            db.session.execute(text("""
                ALTER TABLE exercise_progress
                ADD COLUMN IF NOT EXISTS level VARCHAR(10)
            """))
            db.session.commit()

            # Set NOT NULL after adding (in case there were records)
            db.session.execute(text("""
                ALTER TABLE exercise_progress
                ALTER COLUMN level SET NOT NULL
            """))
            db.session.commit()
            print("[SUCCESS] Added level column to exercise_progress")

            # Step 3: Add level column to topic_progress
            print("\n[Step 3/5] Adding level column to topic_progress table...")
            db.session.execute(text("""
                ALTER TABLE topic_progress
                ADD COLUMN IF NOT EXISTS level VARCHAR(10)
            """))
            db.session.commit()

            # Set NOT NULL after adding
            db.session.execute(text("""
                ALTER TABLE topic_progress
                ALTER COLUMN level SET NOT NULL
            """))
            db.session.commit()
            print("[SUCCESS] Added level column to topic_progress")

            # Step 4: Drop old unique constraints and create new ones for exercise_progress
            print("\n[Step 4/5] Updating unique constraints for exercise_progress...")

            # Drop old constraint if exists
            db.session.execute(text("""
                ALTER TABLE exercise_progress
                DROP CONSTRAINT IF EXISTS _user_topic_exercise_uc
            """))
            db.session.commit()

            # Create new constraint with level
            db.session.execute(text("""
                ALTER TABLE exercise_progress
                ADD CONSTRAINT _user_level_topic_exercise_uc
                UNIQUE (user_progress_id, level, topic_number, exercise_type)
            """))
            db.session.commit()
            print("[SUCCESS] Updated unique constraint for exercise_progress")

            # Step 5: Drop old unique constraints and create new ones for topic_progress
            print("\n[Step 5/5] Updating unique constraints for topic_progress...")

            # Drop old constraint if exists
            db.session.execute(text("""
                ALTER TABLE topic_progress
                DROP CONSTRAINT IF EXISTS _user_topic_uc
            """))
            db.session.commit()

            # Create new constraint with level
            db.session.execute(text("""
                ALTER TABLE topic_progress
                ADD CONSTRAINT _user_level_topic_uc
                UNIQUE (user_progress_id, level, topic_number)
            """))
            db.session.commit()
            print("[SUCCESS] Updated unique constraint for topic_progress")

            print("\n" + "="*50)
            print("Migration Completed Successfully!")
            print("="*50)
            print("\nSummary:")
            print("- Added 'level' column to exercise_progress table")
            print("- Added 'level' column to topic_progress table")
            print("- Updated unique constraints to include level")
            print("- Cleared all existing progress data for fresh start")
            print("\nProgress is now tracked independently per level!")

        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Migration failed: {e}")
            print("\nFull traceback:")
            traceback.print_exc()
            return False

    return True

if __name__ == "__main__":
    success = run_migration()
    if not success:
        sys.exit(1)