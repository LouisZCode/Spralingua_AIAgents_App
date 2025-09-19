"""
Migration 06: Add Exercise Progress Tracking System
This migration adds the exercise_progress table and updates user_progress with current_topic field
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from sqlalchemy import text

def create_exercise_progress_table():
    """Create the exercise_progress table"""

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS exercise_progress (
        id SERIAL PRIMARY KEY,
        user_progress_id INTEGER NOT NULL REFERENCES user_progress(id) ON DELETE CASCADE,
        topic_number INTEGER NOT NULL,
        exercise_type VARCHAR(50) NOT NULL,
        score FLOAT DEFAULT 0.0 NOT NULL,
        completed BOOLEAN DEFAULT FALSE NOT NULL,
        attempts INTEGER DEFAULT 0 NOT NULL,
        best_score FLOAT DEFAULT 0.0 NOT NULL,
        completed_at TIMESTAMP,
        last_attempt_at TIMESTAMP,
        messages_correct INTEGER DEFAULT 0,
        messages_total INTEGER DEFAULT 0,
        UNIQUE(user_progress_id, topic_number, exercise_type)
    );
    """

    # Create indexes for performance
    create_indexes_sql = """
    CREATE INDEX IF NOT EXISTS idx_exercise_progress_user ON exercise_progress(user_progress_id);
    CREATE INDEX IF NOT EXISTS idx_exercise_progress_topic ON exercise_progress(topic_number);
    CREATE INDEX IF NOT EXISTS idx_exercise_progress_completed ON exercise_progress(completed);
    """

    try:
        db.session.execute(text(create_table_sql))
        db.session.execute(text(create_indexes_sql))
        db.session.commit()
        print("[SUCCESS] Created exercise_progress table with indexes")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Creating exercise_progress table: {e}")
        return False

def add_current_topic_to_user_progress():
    """Add current_topic column to user_progress table"""

    # Check if column already exists
    check_column_sql = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name='user_progress' AND column_name='current_topic';
    """

    try:
        result = db.session.execute(text(check_column_sql))
        if result.fetchone():
            print("[INFO] Column current_topic already exists in user_progress table")
            return True

        # Add the column
        add_column_sql = """
        ALTER TABLE user_progress
        ADD COLUMN current_topic INTEGER DEFAULT 1 NOT NULL;
        """

        db.session.execute(text(add_column_sql))
        db.session.commit()
        print("[SUCCESS] Added current_topic column to user_progress table")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Adding current_topic column: {e}")
        return False

def initialize_existing_user_topics():
    """Initialize current_topic for existing user_progress records"""

    update_sql = """
    UPDATE user_progress
    SET current_topic = 1
    WHERE current_topic IS NULL;
    """

    try:
        result = db.session.execute(text(update_sql))
        db.session.commit()
        rows_updated = result.rowcount
        print(f"[SUCCESS] Updated {rows_updated} existing user_progress records with current_topic = 1")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Initializing existing user topics: {e}")
        return False

def verify_migration():
    """Verify the migration was successful"""

    try:
        # Check exercise_progress table
        check_table_sql = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'exercise_progress'
        );
        """
        result = db.session.execute(text(check_table_sql))
        if not result.scalar():
            print("[ERROR] exercise_progress table does not exist")
            return False

        # Check current_topic column
        check_column_sql = """
        SELECT EXISTS (
            SELECT FROM information_schema.columns
            WHERE table_name = 'user_progress'
            AND column_name = 'current_topic'
        );
        """
        result = db.session.execute(text(check_column_sql))
        if not result.scalar():
            print("[ERROR] current_topic column does not exist in user_progress")
            return False

        print("[SUCCESS] Migration verification passed")
        return True

    except Exception as e:
        print(f"[ERROR] Verifying migration: {e}")
        return False

def main():
    """Run the migration"""
    print("\n" + "="*60)
    print("MIGRATION 06: Add Exercise Progress Tracking System")
    print("="*60 + "\n")

    with app.app_context():
        success = True

        # Step 1: Create exercise_progress table
        print("\nStep 1: Creating exercise_progress table...")
        if not create_exercise_progress_table():
            success = False

        # Step 2: Add current_topic to user_progress
        print("\nStep 2: Adding current_topic column to user_progress...")
        if not add_current_topic_to_user_progress():
            success = False

        # Step 3: Initialize existing records
        print("\nStep 3: Initializing existing user records...")
        if not initialize_existing_user_topics():
            success = False

        # Step 4: Verify migration
        print("\nStep 4: Verifying migration...")
        if not verify_migration():
            success = False

        # Final status
        print("\n" + "="*60)
        if success:
            print("[SUCCESS] Migration 06 completed successfully!")
            print("\nNew features added:")
            print("- exercise_progress table for tracking individual exercises")
            print("- current_topic field in user_progress for topic navigation")
            print("- Indexes for performance optimization")
        else:
            print("[WARNING] Migration 06 completed with some issues")
            print("Please review the errors above and fix manually if needed")
        print("="*60 + "\n")

        return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)