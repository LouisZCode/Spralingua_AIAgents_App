"""
Migration script to initialize missing topic_progress records for existing users.
This fixes users who were created before topic initialization was properly implemented.
"""

from app import app
from database import db
from models.user_progress import UserProgress
from models.topic_progress import TopicProgress
from topics.topic_manager import TopicManager

def fix_missing_topics():
    """Initialize missing topic_progress records for all existing users."""
    with app.app_context():
        print("[MIGRATION] Starting topic initialization for existing users...")

        # Get all user_progress records
        all_progress = UserProgress.query.all()
        print(f"[INFO] Found {len(all_progress)} user progress records to check")

        topic_mgr = TopicManager()
        fixed_count = 0
        already_ok = 0
        failed_count = 0

        for progress in all_progress:
            # Check if this progress has topic records
            topic_count = TopicProgress.query.filter_by(
                user_progress_id=progress.id
            ).count()

            print(f"\n[CHECK] User progress {progress.id} (user {progress.user_id})")
            print(f"  Languages: {progress.input_language} -> {progress.target_language}")
            print(f"  Level: {progress.current_level}")
            print(f"  Topics found: {topic_count}")

            if topic_count == 0:
                # Initialize topics for this progress
                print(f"  [FIX] Initializing topics...")
                success, message = topic_mgr.initialize_user_topics(
                    progress.id,
                    progress.current_level
                )

                if success:
                    # Verify topics were created
                    new_count = TopicProgress.query.filter_by(
                        user_progress_id=progress.id
                    ).count()
                    print(f"  [SUCCESS] Created {new_count} topic records")
                    fixed_count += 1
                else:
                    print(f"  [ERROR] Failed to initialize: {message}")
                    failed_count += 1
            else:
                print(f"  [OK] Topics already initialized")
                already_ok += 1

        print("\n" + "="*50)
        print("[MIGRATION COMPLETE]")
        print(f"  Already OK: {already_ok}")
        print(f"  Fixed: {fixed_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Total: {len(all_progress)}")
        print("="*50)

        # Show detailed status for user 5 specifically
        user5_progress = UserProgress.query.filter_by(user_id=5).first()
        if user5_progress:
            print(f"\n[USER 5 STATUS]")
            topics = TopicProgress.query.filter_by(
                user_progress_id=user5_progress.id
            ).order_by(TopicProgress.topic_number).all()

            print(f"  User progress ID: {user5_progress.id}")
            print(f"  Topic records: {len(topics)}")
            if topics:
                for topic in topics[:3]:  # Show first 3 as sample
                    print(f"    Topic {topic.topic_number}: exercises={topic.exercises_completed}/{topic.total_exercises}")

        return fixed_count, failed_count

if __name__ == "__main__":
    fixed, failed = fix_missing_topics()
    exit(0 if failed == 0 else 1)