"""
Run Migration on Production Database
Adds scenario translation columns to production topic_definitions table
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_production_migration():
    """Add multilingual scenario columns to production database"""

    # Use Railway production database directly
    database_url = 'postgresql://postgres:PtoHSNwAQpMSBDuwknCFAGHWbycmQrDt@nozomi.proxy.rlwy.net:38673/railway'

    print(f"[INFO] Using Railway production database")

    print("\n" + "="*80)
    print("PRODUCTION MIGRATION: Add Scenario Translation Columns")
    print("="*80)
    print(f"[INFO] Target database: {database_url[:50]}...")

    try:
        # Connect to production database
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        print("\n[STEP 1] Checking current schema...")

        # Check if columns already exist
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'topic_definitions'
            AND column_name IN ('scenario_spanish', 'scenario_german', 'scenario_portuguese')
        """)

        existing_columns = [row[0] for row in cur.fetchall()]

        if len(existing_columns) == 3:
            print("[INFO] All three columns already exist. Migration not needed.")
            cur.close()
            conn.close()
            return True

        if existing_columns:
            print(f"[WARNING] Some columns already exist: {existing_columns}")
            print("[INFO] Will only add missing columns")

        print("\n[STEP 2] Adding multilingual scenario columns...")

        # Add columns if they don't exist
        columns_to_add = [
            ('scenario_spanish', 'TEXT'),
            ('scenario_german', 'TEXT'),
            ('scenario_portuguese', 'TEXT')
        ]

        for col_name, col_type in columns_to_add:
            if col_name not in existing_columns:
                try:
                    cur.execute(f"""
                        ALTER TABLE topic_definitions
                        ADD COLUMN {col_name} {col_type};
                    """)
                    print(f"  [SUCCESS] Added column: {col_name}")
                except Exception as e:
                    print(f"  [ERROR] Failed to add {col_name}: {e}")
                    conn.rollback()
                    return False

        # Commit the changes
        conn.commit()

        print("\n[STEP 3] Verifying schema changes...")

        # Verify all columns now exist
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'topic_definitions'
            AND column_name IN ('scenario_spanish', 'scenario_german', 'scenario_portuguese')
            ORDER BY column_name
        """)

        new_columns = cur.fetchall()

        if len(new_columns) == 3:
            print("[SUCCESS] All three columns verified:")
            for col_name, col_type in new_columns:
                print(f"  - {col_name}: {col_type}")
        else:
            print(f"[ERROR] Expected 3 columns, found {len(new_columns)}")
            return False

        # Close connection
        cur.close()
        conn.close()

        print("\n" + "="*80)
        print("MIGRATION COMPLETE")
        print("="*80)
        print("[SUCCESS] Production database schema updated")
        print("[INFO] Ready to run sync_databases.py")

        return True

    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    import sys

    print("\n[WARNING] This will modify the PRODUCTION database schema!")
    print("[INFO] This is a safe operation - it only ADDS columns, does not delete data")
    print("\nPress Ctrl+C within 3 seconds to cancel...")

    import time
    try:
        for i in range(3, 0, -1):
            print(f"  {i}...", end='', flush=True)
            time.sleep(1)
        print("\n")
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Migration aborted by user")
        sys.exit(1)

    success = run_production_migration()
    sys.exit(0 if success else 1)
