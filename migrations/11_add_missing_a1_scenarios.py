#!/usr/bin/env python
"""
Migration: Add Missing A1 Scenario Templates
Adds scenario templates for 11 A1 topics that don't have them yet
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_definition import TopicDefinition
from app import app

def add_missing_a1_scenarios():
    """Add scenario templates for A1 topics that don't have them."""

    with app.app_context():
        # Define scenarios for each missing A1 topic
        scenarios = {
            2: "You're at a language exchange café and someone asks about your job and where you're from.",
            3: "You're on the phone trying to book a table at a restaurant and need to spell your name.",
            5: "You're at a pharmacy picking up medicine and need to confirm your name and prescription details.",
            6: "You're at a birthday party and people are talking about their ages and phone numbers.",
            7: "You're at a local market shopping for fruits and vegetables, asking about prices.",
            9: "You're ordering food delivery and need to give your address and directions to your home.",
            10: "You're filling out a gym membership form with help from the receptionist.",
            11: "You're showing family photos on your phone to a new friend who asks about your family members.",
            13: "You're at a park talking to another parent about what your family members like to do on weekends.",
            14: "You're planning to meet a friend and discussing what time works best and checking the weather.",
            15: "You're at a doctor's office trying to schedule your next appointment."
        }

        print("[INFO] Starting to add missing A1 scenarios...")

        # Update each topic with its scenario
        for topic_num, scenario in scenarios.items():
            topic = TopicDefinition.query.filter_by(
                level='A1',
                topic_number=topic_num
            ).first()

            if topic:
                if topic.scenario_template is None:
                    topic.scenario_template = scenario
                    print(f"[SUCCESS] Added scenario for A1 Topic {topic_num}: {topic.title_key}")
                else:
                    print(f"[INFO] A1 Topic {topic_num} already has a scenario, skipping")
            else:
                print(f"[ERROR] A1 Topic {topic_num} not found in database")

        # Commit all changes
        try:
            db.session.commit()
            print("[SUCCESS] All missing A1 scenarios added successfully!")

            # Verify the updates
            print("\n[INFO] Verifying updates...")
            topics_without_scenarios = TopicDefinition.query.filter_by(
                level='A1'
            ).filter(
                TopicDefinition.scenario_template.is_(None)
            ).count()

            if topics_without_scenarios == 0:
                print("[SUCCESS] All A1 topics now have scenario templates!")
            else:
                print(f"[WARNING] {topics_without_scenarios} A1 topics still missing scenarios")

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to commit changes: {e}")
            return False

        return True

if __name__ == "__main__":
    add_missing_a1_scenarios()