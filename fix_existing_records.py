# Fix existing topic_progress records to have has_seen_completion_popup field
# Run this once to update all existing records

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from sqlalchemy import text

def fix_existing_records():
    """Update existing topic_progress records with default value for has_seen_completion_popup"""

    with app.app_context():
        try:
            # First check if the column exists
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='topic_progress'
                AND column_name='has_seen_completion_popup'
            """))

            if not result.fetchone():
                print("[ERROR] Column 'has_seen_completion_popup' doesn't exist. Run migration first.")
                return False

            # Update all existing records to have the default value
            # For completed topics, set to False so popup can show
            # For incomplete topics, also set to False (doesn't matter)
            db.session.execute(text("""
                UPDATE topic_progress
                SET has_seen_completion_popup = FALSE
                WHERE has_seen_completion_popup IS NULL
            """))

            db.session.commit()
            print("[SUCCESS] Updated all existing topic_progress records")

            # Check how many records were updated
            result = db.session.execute(text("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN completed = TRUE THEN 1 ELSE 0 END) as completed_topics
                FROM topic_progress
            """))

            row = result.fetchone()
            print(f"[INFO] Total topic records: {row[0]}")
            print(f"[INFO] Completed topics that can show popup: {row[1]}")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to update records: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("Fix Existing Topic Progress Records")
    print("=" * 60)

    success = fix_existing_records()

    if success:
        print("\n[SUCCESS] All existing records updated!")
        print("[INFO] The popup should now work for completed topics")
    else:
        print("\n[ERROR] Failed to update records")
        sys.exit(1)