"""
Migration: Add multilingual scenario columns to topic_definitions table

Adds three new columns for storing scenario translations:
- scenario_spanish (TEXT)
- scenario_german (TEXT)
- scenario_portuguese (TEXT)

This allows each topic to have scenarios in all 4 supported languages.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Add language-specific scenario columns to topic_definitions"""

    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("[ERROR] DATABASE_URL not found in environment variables")
        return False

    # Convert postgres:// to postgresql:// if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        print("[INFO] Adding scenario translation columns to topic_definitions...")

        # Add Spanish scenario column
        print("[INFO] Adding scenario_spanish column...")
        cur.execute("""
            ALTER TABLE topic_definitions
            ADD COLUMN IF NOT EXISTS scenario_spanish TEXT;
        """)

        # Add German scenario column
        print("[INFO] Adding scenario_german column...")
        cur.execute("""
            ALTER TABLE topic_definitions
            ADD COLUMN IF NOT EXISTS scenario_german TEXT;
        """)

        # Add Portuguese scenario column
        print("[INFO] Adding scenario_portuguese column...")
        cur.execute("""
            ALTER TABLE topic_definitions
            ADD COLUMN IF NOT EXISTS scenario_portuguese TEXT;
        """)

        # Commit changes
        conn.commit()

        # Verify columns were added
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'topic_definitions'
            AND column_name LIKE 'scenario_%'
            ORDER BY column_name;
        """)

        columns = cur.fetchall()
        print(f"\n[SUCCESS] Migration completed! Scenario columns in topic_definitions:")
        for col in columns:
            print(f"  - {col[0]}")

        # Close connection
        cur.close()
        conn.close()

        return True

    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("="*60)
    print("MIGRATION: Add Scenario Translation Columns")
    print("="*60)

    success = run_migration()

    if success:
        print("\n[COMPLETE] Migration successful!")
    else:
        print("\n[FAILED] Migration failed. Check errors above.")
