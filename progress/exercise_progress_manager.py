# Exercise Progress Manager for Spralingua
# Handles tracking of individual exercise completion within topics

from database import db
from models.exercise_progress import ExerciseProgress
from models.topic_progress import TopicProgress
from models.user_progress import UserProgress
from sqlalchemy.exc import IntegrityError

class ExerciseProgressManager:
    """Manages exercise completion tracking and topic advancement"""

    def __init__(self):
        """Initialize the ExerciseProgressManager"""
        self.db = db

    def get_exercise_progress(self, user_progress_id, topic_number, exercise_type):
        """
        Get specific exercise progress for a user

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic number (1-12)
            exercise_type: The exercise type ('casual_chat', 'email_writing', etc.)

        Returns:
            ExerciseProgress object or None
        """
        try:
            progress = ExerciseProgress.query.filter_by(
                user_progress_id=user_progress_id,
                topic_number=topic_number,
                exercise_type=exercise_type.lower()
            ).first()
            return progress
        except Exception as e:
            print(f"[ERROR] Getting exercise progress: {e}")
            return None

    def record_exercise_attempt(self, user_progress_id, topic_number, exercise_type,
                               score, messages_correct=None, messages_total=None):
        """
        Record an exercise attempt and check for topic completion

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic number (1-12)
            exercise_type: The exercise type
            score: The score achieved (0-100)
            messages_correct: Optional - for casual chat
            messages_total: Optional - for casual chat

        Returns:
            dict with results including completion status
        """
        try:
            # Get or create exercise progress record
            exercise_progress = self.get_exercise_progress(
                user_progress_id, topic_number, exercise_type
            )

            if not exercise_progress:
                # Create new record
                exercise_progress = ExerciseProgress(
                    user_progress_id=user_progress_id,
                    topic_number=topic_number,
                    exercise_type=exercise_type
                )
                self.db.session.add(exercise_progress)

            # Record the attempt
            was_completed = exercise_progress.completed
            is_now_complete = exercise_progress.record_attempt(
                score, messages_correct, messages_total
            )

            # Commit the exercise progress
            self.db.session.commit()

            # Check if this completion triggers topic advancement
            topic_advanced = False
            if is_now_complete and not was_completed:
                topic_advanced = self._check_topic_completion(user_progress_id, topic_number)

            return {
                'success': True,
                'exercise_progress': exercise_progress.to_dict(),
                'newly_completed': is_now_complete and not was_completed,
                'topic_advanced': topic_advanced
            }

        except IntegrityError as e:
            self.db.session.rollback()
            return {'success': False, 'error': 'Database integrity error'}
        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] Recording exercise attempt: {e}")
            return {'success': False, 'error': str(e)}

    def _check_topic_completion(self, user_progress_id, topic_number):
        """
        Check if all exercises in a topic are complete and advance if so

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic number to check

        Returns:
            bool: True if topic was completed and user advanced
        """
        try:
            # Get all exercises for this topic
            # Currently we have 2 active exercises: casual_chat and email_writing
            active_exercises = ['casual_chat', 'email_writing']

            all_complete = True
            for exercise_type in active_exercises:
                progress = self.get_exercise_progress(
                    user_progress_id, topic_number, exercise_type
                )
                if not progress or not progress.completed:
                    all_complete = False
                    break

            if all_complete:
                print(f"[INFO] All exercises complete for topic {topic_number}. Marking topic complete.")

                # Use TopicManager to handle topic completion properly
                from topics.topic_manager import TopicManager
                topic_manager = TopicManager()
                success, result = topic_manager.mark_topic_complete(user_progress_id, topic_number)

                if success:
                    print(f"[SUCCESS] Topic {topic_number} marked as complete")
                    # Log next item info
                    if result.get('next_item'):
                        next_item = result['next_item']
                        if next_item['type'] == 'topic':
                            print(f"[INFO] Next topic: Topic {next_item['topic_number']}")
                        elif next_item['type'] == 'test':
                            print(f"[INFO] Next: {next_item['message']}")
                        elif next_item['type'] == 'completed':
                            print(f"[INFO] Level completed!")
                    return True
                else:
                    print(f"[ERROR] Failed to mark topic complete: {result}")
                    return False

            return False

        except Exception as e:
            print(f"[ERROR] Checking topic completion: {e}")
            self.db.session.rollback()
            return False

    def _calculate_level_progress(self, user_progress_id):
        """
        Calculate overall progress percentage in current level

        Args:
            user_progress_id: The user progress ID

        Returns:
            int: Progress percentage (0-100)
        """
        try:
            # Count completed topics
            completed_topics = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id,
                completed=True
            ).count()

            # 16 total points: 12 topics + 4 tests
            # For now, just count topics (tests will be added later)
            progress = int((completed_topics / 12) * 100)
            return min(100, progress)

        except Exception as e:
            print(f"[ERROR] Calculating level progress: {e}")
            return 0

    def get_topic_exercises_status(self, user_progress_id, topic_number):
        """
        Get status of all exercises in a topic

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic number

        Returns:
            dict with exercise statuses
        """
        try:
            active_exercises = ['casual_chat', 'email_writing']
            exercises_status = {}

            for exercise_type in active_exercises:
                progress = self.get_exercise_progress(
                    user_progress_id, topic_number, exercise_type
                )

                if progress:
                    exercises_status[exercise_type] = {
                        'completed': progress.completed,
                        'score': progress.score,
                        'best_score': progress.best_score,
                        'attempts': progress.attempts,
                        'status': progress.get_completion_status()
                    }
                else:
                    exercises_status[exercise_type] = {
                        'completed': False,
                        'score': 0,
                        'best_score': 0,
                        'attempts': 0,
                        'status': 'not_started'
                    }

            # Check if topic is complete
            topic_complete = all(ex['completed'] for ex in exercises_status.values())

            return {
                'exercises': exercises_status,
                'topic_complete': topic_complete,
                'topic_number': topic_number
            }

        except Exception as e:
            print(f"[ERROR] Getting topic exercises status: {e}")
            return {
                'exercises': {},
                'topic_complete': False,
                'topic_number': topic_number
            }

    def reset_exercise_progress(self, user_progress_id, topic_number, exercise_type):
        """
        Reset progress for a specific exercise (for testing)

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic number
            exercise_type: The exercise type

        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            progress = self.get_exercise_progress(
                user_progress_id, topic_number, exercise_type
            )

            if progress:
                progress.reset_progress()
                self.db.session.commit()
                return True, 'Exercise progress reset successfully'
            else:
                return False, 'Exercise progress not found'

        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] Resetting exercise progress: {e}")
            return False, f'Error resetting progress: {str(e)}'

    def get_all_exercises_for_user(self, user_progress_id):
        """
        Get all exercise progress records for a user

        Args:
            user_progress_id: The user progress ID

        Returns:
            List of ExerciseProgress objects
        """
        try:
            exercises = ExerciseProgress.query.filter_by(
                user_progress_id=user_progress_id
            ).order_by(
                ExerciseProgress.topic_number,
                ExerciseProgress.exercise_type
            ).all()
            return exercises
        except Exception as e:
            print(f"[ERROR] Getting all exercises for user: {e}")
            return []