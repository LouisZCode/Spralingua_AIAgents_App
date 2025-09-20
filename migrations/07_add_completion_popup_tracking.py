# Migration: Add completion popup tracking to topic_progress table
# This adds a field to track whether users have seen the completion popup for each topic

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from sqlalchemy import text

def add_completion_popup_tracking():
    """Add has_seen_completion_popup field to topic_progress table"""

    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='topic_progress'
                AND column_name='has_seen_completion_popup'
            """))

            if result.fetchone():
                print("[INFO] Column 'has_seen_completion_popup' already exists")
                return True

            # Add the new column
            db.session.execute(text("""
                ALTER TABLE topic_progress
                ADD COLUMN has_seen_completion_popup BOOLEAN DEFAULT FALSE NOT NULL
            """))

            db.session.commit()
            print("[SUCCESS] Added 'has_seen_completion_popup' column to topic_progress table")

            # Verify the column was added
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='topic_progress'
                AND column_name='has_seen_completion_popup'
            """))

            if result.fetchone():
                print("[SUCCESS] Column verified in database")
            else:
                print("[WARNING] Column not found after adding - please check database")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to add completion popup tracking: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("Migration: Add Completion Popup Tracking")
    print("=" * 60)

    success = add_completion_popup_tracking()

    if success:
        print("\n[SUCCESS] Migration completed successfully!")
    else:
        print("\n[ERROR] Migration failed!")
        sys.exit(1)