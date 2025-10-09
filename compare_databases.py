#!/usr/bin/env python
"""
Database Comparison Script
Compares local development database with Railway production database
Identifies discrepancies in structure and content
"""

import os
import sys
import json
from sqlalchemy import create_engine, text
from tabulate import tabulate

# Database connection strings
LOCAL_DB = "postgresql://dev:devpass@localhost:5432/spralingua_dev"
PRODUCTION_DB = os.getenv('DATABASE_URL', 'postgresql://postgres:PtoHSNwAQpMSBDuwknCFAGHWbycmQrDt@nozomi.proxy.rlwy.net:38673/railway')

def get_connection(db_url):
    """Create database connection"""
    return create_engine(db_url)

def compare_table_counts(local_conn, prod_conn):
    """Compare row counts for all tables"""
    print("\n" + "="*80)
    print("TABLE ROW COUNTS COMPARISON")
    print("="*80)

    tables = [
        'users', 'user_progress', 'topic_definitions', 'level_rules',
        'exercise_types', 'topic_exercises', 'topic_progress',
        'test_progress', 'exercise_progress'
    ]

    results = []
    for table in tables:
        try:
            local_count = local_conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            prod_count = prod_conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()

            status = "[MATCH]" if local_count == prod_count else "[DIFFER]"
            results.append([table, local_count, prod_count, status])
        except Exception as e:
            results.append([table, "ERROR", "ERROR", str(e)[:30]])

    print(tabulate(results, headers=['Table', 'Local', 'Production', 'Status'], tablefmt='grid'))

def compare_topic_definitions(local_conn, prod_conn):
    """Deep comparison of topic_definitions table"""
    print("\n" + "="*80)
    print("TOPIC DEFINITIONS DETAILED COMPARISON")
    print("="*80)

    # Compare topic counts by level
    print("\n[INFO] Topics per level:")
    for level in ['A1', 'A2', 'B1', 'B2']:
        local_count = local_conn.execute(
            text("SELECT COUNT(*) FROM topic_definitions WHERE level = :level"),
            {"level": level}
        ).scalar()
        prod_count = prod_conn.execute(
            text("SELECT COUNT(*) FROM topic_definitions WHERE level = :level"),
            {"level": level}
        ).scalar()

        status = "[OK]" if local_count == prod_count else "[X]"
        print(f"  {status} {level}: Local={local_count}, Production={prod_count}")

    # Compare critical columns for A1 Topic 1 (the problematic one)
    print("\n[INFO] A1 Topic 1 Detailed Comparison:")

    columns_to_check = [
        'title_key', 'llm_prompt_template', 'word_limit',
        'number_of_exchanges', 'scenario_template', 'conversation_flow'
    ]

    local_topic1 = local_conn.execute(
        text(f"SELECT {', '.join(columns_to_check)} FROM topic_definitions WHERE level='A1' AND topic_number=1")
    ).fetchone()

    prod_topic1 = prod_conn.execute(
        text(f"SELECT {', '.join(columns_to_check)} FROM topic_definitions WHERE level='A1' AND topic_number=1")
    ).fetchone()

    if local_topic1 and prod_topic1:
        differences = []
        for i, col in enumerate(columns_to_check):
            local_val = str(local_topic1[i])[:100] if local_topic1[i] else "NULL"
            prod_val = str(prod_topic1[i])[:100] if prod_topic1[i] else "NULL"

            match = "[OK]" if local_val == prod_val else "[X]"
            differences.append([col, match, local_val, prod_val])

        print(tabulate(differences, headers=['Column', 'Match', 'Local (first 100 chars)', 'Production (first 100 chars)'], tablefmt='grid'))

    # Check for NULL fields across all topics
    print("\n[INFO] NULL field analysis across all topics:")

    nullable_columns = ['scenario_template', 'conversation_flow', 'word_limit',
                        'opening_phrases', 'required_vocabulary', 'topic_specific_rules']

    for col in nullable_columns:
        local_nulls = local_conn.execute(
            text(f"SELECT COUNT(*) FROM topic_definitions WHERE {col} IS NULL")
        ).scalar()
        prod_nulls = prod_conn.execute(
            text(f"SELECT COUNT(*) FROM topic_definitions WHERE {col} IS NULL")
        ).scalar()

        status = "[OK]" if local_nulls == prod_nulls else "[X]"
        print(f"  {status} {col}: Local NULLs={local_nulls}, Production NULLs={prod_nulls}")

def compare_level_rules(local_conn, prod_conn):
    """Compare level_rules table"""
    print("\n" + "="*80)
    print("LEVEL RULES COMPARISON")
    print("="*80)

    for level in ['A1', 'A2', 'B1', 'B2']:
        print(f"\n[INFO] {level} Level Rules:")

        local_rule = local_conn.execute(
            text("SELECT base_word_limit, grammar_rules, general_guidelines FROM level_rules WHERE level = :level"),
            {"level": level}
        ).fetchone()

        prod_rule = prod_conn.execute(
            text("SELECT base_word_limit, grammar_rules, general_guidelines FROM level_rules WHERE level = :level"),
            {"level": level}
        ).fetchone()

        if local_rule and prod_rule:
            # Compare word limits
            word_match = "[OK]" if local_rule[0] == prod_rule[0] else "[X]"
            print(f"  {word_match} Base Word Limit: Local={local_rule[0]}, Production={prod_rule[0]}")

            # Compare grammar rules (JSON)
            local_grammar = json.loads(local_rule[1]) if isinstance(local_rule[1], str) else local_rule[1]
            prod_grammar = json.loads(prod_rule[1]) if isinstance(prod_rule[1], str) else prod_rule[1]
            grammar_match = "[OK]" if local_grammar == prod_grammar else "[X]"
            print(f"  {grammar_match} Grammar Rules: {grammar_match}")

            # Compare guidelines (first 100 chars)
            local_guide = str(local_rule[2])[:100]
            prod_guide = str(prod_rule[2])[:100]
            guide_match = "[OK]" if local_guide == prod_guide else "[X]"
            print(f"  {guide_match} Guidelines Match: {guide_match}")
        else:
            print(f"  [X] Missing in one or both databases!")

def export_topic_differences(local_conn, prod_conn):
    """Export full topic definitions for A1 topics that differ"""
    print("\n" + "="*80)
    print("EXPORTING A1 TOPIC DIFFERENCES TO FILE")
    print("="*80)

    output_file = "topic_differences_a1.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("A1 TOPIC DEFINITIONS FULL COMPARISON\n")
        f.write("="*80 + "\n\n")

        for topic_num in range(1, 17):
            local_topic = local_conn.execute(
                text("SELECT * FROM topic_definitions WHERE level='A1' AND topic_number=:num"),
                {"num": topic_num}
            ).fetchone()

            prod_topic = prod_conn.execute(
                text("SELECT * FROM topic_definitions WHERE level='A1' AND topic_number=:num"),
                {"num": topic_num}
            ).fetchone()

            if local_topic and prod_topic:
                # Get column names
                columns = local_conn.execute(
                    text("SELECT column_name FROM information_schema.columns WHERE table_name='topic_definitions' ORDER BY ordinal_position")
                ).fetchall()
                col_names = [c[0] for c in columns]

                f.write(f"\n{'='*80}\n")
                f.write(f"TOPIC {topic_num}\n")
                f.write(f"{'='*80}\n\n")

                for i, col in enumerate(col_names):
                    if i < len(local_topic) and i < len(prod_topic):
                        local_val = local_topic[i]
                        prod_val = prod_topic[i]

                        match = "[OK]" if local_val == prod_val else "[X]"

                        f.write(f"{match} {col}:\n")
                        f.write(f"  LOCAL: {local_val}\n")
                        f.write(f"  PROD:  {prod_val}\n\n")

    print(f"[SUCCESS] Exported to {output_file}")

def main():
    """Run all comparisons"""
    print("\n" + "="*80)
    print("DATABASE COMPARISON: Local vs Production")
    print("="*80)
    print(f"Local:      {LOCAL_DB}")
    print(f"Production: {PRODUCTION_DB[:50]}...")

    try:
        # Create connections
        local_engine = get_connection(LOCAL_DB)
        prod_engine = get_connection(PRODUCTION_DB)

        with local_engine.connect() as local_conn, prod_engine.connect() as prod_conn:
            # Run comparisons
            compare_table_counts(local_conn, prod_conn)
            compare_topic_definitions(local_conn, prod_conn)
            compare_level_rules(local_conn, prod_conn)
            export_topic_differences(local_conn, prod_conn)

        print("\n" + "="*80)
        print("COMPARISON COMPLETE")
        print("="*80)
        print("[INFO] Check 'topic_differences_a1.txt' for detailed A1 topic comparison")

    except Exception as e:
        print(f"\n[ERROR] Comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
