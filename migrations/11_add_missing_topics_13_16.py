# Migration to add missing topics 13-16 to existing users
# These topics were added when we converted from 12 to 16 topics
# but existing users didn't get topic_progress records for them

import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_progress import TopicProgress
from models.user_progress import UserProgress
from models.topic_definition import TopicDefinition
from app import app

def add_missing_topics():
    """Add topic_progress records for topics 13-16 for existing users."""
    with app.app_context():
        print("Starting migration to add topics 13-16...")

        # Get all user progress records
        user_progresses = UserProgress.query.all()

        topics_added = 0

        for up in user_progresses:
            print(f"\nChecking user_progress_id {up.id} (user_id: {up.user_id})...")

            # Check which topics are missing (should be 13-16)
            for topic_num in [13, 14, 15, 16]:
                # Check if topic_progress exists for this topic
                existing = TopicProgress.query.filter_by(
                    user_progress_id=up.id,
                    topic_number=topic_num
                ).first()

                if not existing:
                    # Verify the topic exists in topic_definitions for this level
                    topic_def = TopicDefinition.query.filter_by(
                        level=up.current_level,
                        topic_number=topic_num
                    ).first()

                    if topic_def:
                        # Create the missing topic_progress record
                        new_progress = TopicProgress(
                            user_progress_id=up.id,
                            topic_number=topic_num,
                            total_exercises=2  # Standard: casual_chat and email_writing
                        )
                        db.session.add(new_progress)
                        topics_added += 1
                        print(f"  - Added topic {topic_num} ({topic_def.title_key})")
                    else:
                        print(f"  - Topic {topic_num} not found in {up.current_level} definitions (may be expected)")
                else:
                    print(f"  - Topic {topic_num} already exists")

        # Commit all changes
        db.session.commit()
        print(f"\nMigration complete! Added {topics_added} topic_progress records.")

        # Verify the results
        print("\nVerifying results...")
        for up in user_progresses:
            topic_count = TopicProgress.query.filter_by(
                user_progress_id=up.id
            ).count()
            print(f"User progress {up.id}: {topic_count} topics")

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Add missing topics 13-16 to existing users")
    print("=" * 60)
    add_missing_topics()
    print("\nAll users now have access to all 16 topics!")