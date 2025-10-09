#!/usr/bin/env python
"""
Complete Database Synchronization Script
Makes production database IDENTICAL to local development database
WARNING: This will DELETE ALL data in production and replace with local data
"""

import os
import sys
import json
from sqlalchemy import create_engine, text

# Database connection strings
LOCAL_DB = "postgresql://dev:devpass@localhost:5432/spralingua_dev"
PRODUCTION_DB = os.getenv('DATABASE_URL', 'postgresql://postgres:PtoHSNwAQpMSBDuwknCFAGHWbycmQrDt@nozomi.proxy.rlwy.net:38673/railway')

def sync_databases():
    """Sync all tables from local to production"""

    print("\n" + "="*80)
    print("DATABASE SYNCHRONIZATION: Local -> Production")
    print("="*80)
    print("[WARNING] This will DELETE ALL production data and replace with local data")
    print("[WARNING] Test user (Luis) and all progress will be DELETED")
    print("="*80)

    # Tables to sync in order (respecting foreign keys)
    tables_in_order = [
        'users',
        'user_progress',
        'level_rules',
        'exercise_types',
        'topic_definitions',
        'topic_exercises',
        'topic_progress',
        'test_progress',
        'exercise_progress'
    ]

    try:
        local_engine = create_engine(LOCAL_DB)
        prod_engine = create_engine(PRODUCTION_DB)

        with local_engine.connect() as local_conn, prod_engine.connect() as prod_conn:

            # Step 1: Disable foreign key constraints in production
            print("\n[STEP 1] Disabling foreign key constraints...")
            prod_conn.execute(text("SET session_replication_role = 'replica';"))
            prod_conn.commit()
            print("[SUCCESS] Foreign key constraints disabled")

            # Step 2: Truncate all production tables
            print("\n[STEP 2] Truncating all production tables...")
            for table in tables_in_order:
                try:
                    prod_conn.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
                    print(f"  [OK] Truncated {table}")
                except Exception as e:
                    print(f"  [ERROR] Could not truncate {table}: {e}")
            prod_conn.commit()

            # Step 3: Copy data table by table
            print("\n[STEP 3] Copying data from local to production...")

            for table in tables_in_order:
                print(f"\n  [INFO] Processing table: {table}")

                # Get row count from local
                local_count = local_conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"    Local rows: {local_count}")

                if local_count == 0:
                    print(f"    [SKIP] No data to copy")
                    continue

                # Get column names
                columns_result = local_conn.execute(text(f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = '{table}'
                    ORDER BY ordinal_position
                """))
                columns = [row[0] for row in columns_result]
                column_list = ', '.join(columns)

                # Fetch all data from local
                local_data = local_conn.execute(text(f"SELECT {column_list} FROM {table}")).fetchall()

                # Insert into production
                placeholders = ', '.join([f':{col}' for col in columns])
                insert_query = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"

                for row in local_data:
                    row_dict = dict(zip(columns, row))

                    # Convert dict/list values to JSON strings for PostgreSQL
                    for key, value in row_dict.items():
                        if isinstance(value, (dict, list)):
                            row_dict[key] = json.dumps(value)

                    prod_conn.execute(text(insert_query), row_dict)

                prod_conn.commit()

                # Verify
                prod_count = prod_conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"    Production rows: {prod_count}")

                if prod_count == local_count:
                    print(f"    [SUCCESS] {table} synced ({prod_count} rows)")
                else:
                    print(f"    [WARNING] Row count mismatch! Local={local_count}, Prod={prod_count}")

            # Step 4: Reset sequences (auto-increment IDs)
            print("\n[STEP 4] Resetting sequences...")

            sequences = {
                'users': 'users_id_seq',
                'user_progress': 'user_progress_id_seq',
                'level_rules': 'level_rules_id_seq',
                'exercise_types': 'exercise_types_id_seq',
                'topic_definitions': 'topic_definitions_id_seq',
                'topic_exercises': 'topic_exercises_id_seq',
                'topic_progress': 'topic_progress_id_seq',
                'test_progress': 'test_progress_id_seq',
                'exercise_progress': 'exercise_progress_id_seq'
            }

            for table, seq in sequences.items():
                try:
                    # Get max ID from table
                    max_id = prod_conn.execute(text(f"SELECT MAX(id) FROM {table}")).scalar()
                    if max_id:
                        prod_conn.execute(text(f"SELECT setval('{seq}', {max_id});"))
                        print(f"  [OK] Reset {seq} to {max_id}")
                    else:
                        prod_conn.execute(text(f"SELECT setval('{seq}', 1, false);"))
                        print(f"  [OK] Reset {seq} to 1")
                except Exception as e:
                    print(f"  [WARNING] Could not reset {seq}: {e}")

            prod_conn.commit()

            # Step 5: Re-enable foreign key constraints
            print("\n[STEP 5] Re-enabling foreign key constraints...")
            prod_conn.execute(text("SET session_replication_role = 'origin';"))
            prod_conn.commit()
            print("[SUCCESS] Foreign key constraints re-enabled")

            # Step 6: Final verification
            print("\n[STEP 6] Final verification...")
            print("\nTable counts comparison:")
            print(f"{'Table':<25} {'Local':<10} {'Production':<12} {'Status':<10}")
            print("-" * 60)

            for table in tables_in_order:
                local_count = local_conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                prod_count = prod_conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                status = "[MATCH]" if local_count == prod_count else "[DIFFER]"
                print(f"{table:<25} {local_count:<10} {prod_count:<12} {status:<10}")

            print("\n" + "="*80)
            print("SYNCHRONIZATION COMPLETE")
            print("="*80)
            print("[SUCCESS] Production database is now IDENTICAL to local database")

        return True

    except Exception as e:
        print(f"\n[ERROR] Synchronization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n[WARNING] You are about to REPLACE ALL production data with local data!")
    print("[WARNING] This action is IRREVERSIBLE!")
    print("\nPress Ctrl+C within 5 seconds to cancel...")

    import time
    try:
        for i in range(5, 0, -1):
            print(f"  {i}...", end='', flush=True)
            time.sleep(1)
        print("\n")
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Synchronization aborted by user")
        sys.exit(1)

    success = sync_databases()
    sys.exit(0 if success else 1)
