# Initialize topic progress records for a user
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from topics.topic_manager import TopicManager

with app.app_context():
    # User progress ID 13 (Luis, english->spanish, A1)
    user_progress_id = 13
    level = 'A1'

    topic_mgr = TopicManager()
    success, message = topic_mgr.initialize_user_topics(user_progress_id, level)

    print(f"[INFO] Result: {message}")

    if success:
        print("[SUCCESS] Topics initialized!")

        # Check if user has completed exercises for topic 1
        from models.exercise_progress import ExerciseProgress

        # Check exercise completion
        exercises = ExerciseProgress.query.filter_by(
            user_progress_id=user_progress_id,
            topic_number=1
        ).all()

        print(f"\n[INFO] Topic 1 exercises:")
        for ex in exercises:
            print(f"  - {ex.exercise_type}: {'Completed' if ex.completed else 'Not completed'} (Score: {ex.score}%)")

        # If both exercises are complete, mark topic 1 as complete
        if len(exercises) >= 2 and all(ex.completed for ex in exercises):
            from models.topic_progress import TopicProgress

            topic1 = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id,
                topic_number=1
            ).first()

            if topic1:
                topic1.completed = True
                topic1.exercises_completed = topic1.total_exercises
                topic1.has_seen_completion_popup = False  # So popup will show
                db.session.commit()
                print("\n[SUCCESS] Topic 1 marked as complete!")
                print("[INFO] Popup should appear when you visit Learning Hub")