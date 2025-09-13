# Migration: Add scenario templates to topic definitions
# This adds scenario_template column for dynamic conversation context

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from flask import Flask
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

def run_migration():
    """Add scenario_template column to topic_definitions table"""

    # Database connection parameters
    conn_params = {
        'dbname': 'spralingua_dev',
        'user': 'dev',
        'password': 'devpass',
        'host': 'localhost',
        'port': 5432
    }

    conn = None
    cursor = None

    try:
        # Connect to database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        print("[INFO] Connected to database")

        # Step 1: Add scenario_template column if it doesn't exist
        print("[INFO] Adding scenario_template column...")
        cursor.execute("""
            ALTER TABLE topic_definitions
            ADD COLUMN IF NOT EXISTS scenario_template TEXT;
        """)

        print("[SUCCESS] Column added or already exists")

        # Step 2: Populate A1 Topic 1 with initial scenario
        print("[INFO] Populating A1 Topic 1 scenario...")

        a1_topic1_scenario = """It's your first time practicing {target_language}. You meet someone new at a café. Start by greeting them and introducing yourself with your name."""

        cursor.execute("""
            UPDATE topic_definitions
            SET scenario_template = %s
            WHERE level = 'A1' AND topic_number = 1;
        """, (a1_topic1_scenario,))

        # Check if update was successful
        cursor.execute("""
            SELECT level, topic_number, title_key, scenario_template
            FROM topic_definitions
            WHERE level = 'A1' AND topic_number = 1;
        """)

        result = cursor.fetchone()
        if result and result[3]:
            print(f"[SUCCESS] A1 Topic 1 scenario set: '{result[3][:50]}...'")
        else:
            print("[WARNING] A1 Topic 1 scenario not set")

        # Step 3: Show statistics
        cursor.execute("""
            SELECT
                COUNT(*) as total_topics,
                COUNT(scenario_template) as topics_with_scenarios
            FROM topic_definitions;
        """)

        stats = cursor.fetchone()
        print(f"[INFO] Total topics: {stats[0]}")
        print(f"[INFO] Topics with scenarios: {stats[1]}")
        print(f"[INFO] Topics remaining: {stats[0] - stats[1]}")

        # Commit the changes
        conn.commit()
        print("[SUCCESS] Migration completed successfully!")

        # Show all topics status
        print("\n[INFO] Topics with scenarios:")
        cursor.execute("""
            SELECT level, topic_number, title_key,
                   CASE
                       WHEN scenario_template IS NOT NULL THEN 'Has scenario'
                       ELSE 'No scenario (placeholder)'
                   END as status
            FROM topic_definitions
            ORDER BY
                CASE level
                    WHEN 'A1' THEN 1
                    WHEN 'A2' THEN 2
                    WHEN 'B1' THEN 3
                    WHEN 'B2' THEN 4
                END,
                topic_number
            LIMIT 12;
        """)

        for row in cursor.fetchall():
            print(f"  {row[0]} Topic {row[1]:2d} ({row[2]:20s}): {row[3]}")

    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return True

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Add Scenario Templates to Topics")
    print("=" * 60)
    print("This migration will:")
    print("1. Add scenario_template column to topic_definitions")
    print("2. Populate A1 Topic 1 with initial scenario")
    print("3. Leave other topics empty (to be filled incrementally)")
    print("-" * 60)

    if run_migration():
        print("\n[SUCCESS] Migration completed! A1 Topic 1 now has a scenario template.")
        print("[INFO] Other topics will be populated incrementally as content is developed.")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")