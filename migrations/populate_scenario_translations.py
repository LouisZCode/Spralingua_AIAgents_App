"""
Migration: Populate multilingual scenario translations

Reads translation data from scenario_translations_data.py and populates
the scenario_spanish, scenario_german, and scenario_portuguese columns
in the topic_definitions table.
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

# Add parent directory to path to import translation data
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scenario_translations_data import SCENARIO_TRANSLATIONS

# Load environment variables
load_dotenv()

def populate_translations():
    """Populate scenario translations in topic_definitions table"""

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

        print("[INFO] Populating scenario translations...")
        print(f"[INFO] Total scenarios to update: {len(SCENARIO_TRANSLATIONS)}")

        update_count = 0
        error_count = 0

        # Iterate through all translations
        for (level, topic_number), translations in SCENARIO_TRANSLATIONS.items():
            spanish = translations.get('spanish')
            german = translations.get('german')
            portuguese = translations.get('portuguese')

            try:
                # Update the record
                cur.execute("""
                    UPDATE topic_definitions
                    SET
                        scenario_spanish = %s,
                        scenario_german = %s,
                        scenario_portuguese = %s
                    WHERE level = %s AND topic_number = %s
                """, (spanish, german, portuguese, level, topic_number))

                if cur.rowcount > 0:
                    update_count += 1
                    print(f"[SUCCESS] Updated {level} Topic {topic_number}")
                else:
                    error_count += 1
                    print(f"[WARNING] No record found for {level} Topic {topic_number}")

            except Exception as e:
                error_count += 1
                print(f"[ERROR] Failed to update {level} Topic {topic_number}: {e}")

        # Commit all changes
        conn.commit()

        # Verify updates
        cur.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(scenario_spanish) as spanish_count,
                COUNT(scenario_german) as german_count,
                COUNT(scenario_portuguese) as portuguese_count
            FROM topic_definitions;
        """)

        result = cur.fetchone()
        total, spanish_count, german_count, portuguese_count = result

        print(f"\n[SUMMARY] Migration Results:")
        print(f"  - Successfully updated: {update_count} records")
        print(f"  - Errors: {error_count}")
        print(f"\n[VERIFICATION] Database Status:")
        print(f"  - Total topics: {total}")
        print(f"  - Spanish translations: {spanish_count}")
        print(f"  - German translations: {german_count}")
        print(f"  - Portuguese translations: {portuguese_count}")

        # Sample check: Verify A1 Topic 1 has {target_language} placeholder
        cur.execute("""
            SELECT scenario_spanish, scenario_german, scenario_portuguese
            FROM topic_definitions
            WHERE level = 'A1' AND topic_number = 1;
        """)

        a1_topic1 = cur.fetchone()
        if a1_topic1:
            print(f"\n[PLACEHOLDER CHECK] A1 Topic 1 verification:")
            for idx, lang in enumerate(['Spanish', 'German', 'Portuguese']):
                has_placeholder = '{target_language}' in a1_topic1[idx] if a1_topic1[idx] else False
                status = "✓" if has_placeholder else "✗"
                print(f"  {status} {lang}: {has_placeholder}")

        # Close connection
        cur.close()
        conn.close()

        return error_count == 0

    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("="*60)
    print("MIGRATION: Populate Scenario Translations")
    print("="*60)

    success = populate_translations()

    if success:
        print("\n[COMPLETE] All translations populated successfully!")
    else:
        print("\n[FAILED] Migration completed with errors. Check messages above.")
