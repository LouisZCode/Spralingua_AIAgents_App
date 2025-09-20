# Test Manager for Spralingua
# Handles test progression and gatekeeping

from database import db
from models.test_progress import TestProgress
from models.topic_progress import TopicProgress
from models.user_progress import UserProgress
from sqlalchemy.exc import IntegrityError

class TestManager:
    """Manages test progression and level advancement"""
    
    def __init__(self):
        """Initialize the TestManager"""
        self.db = db
        self.passing_threshold = 50  # Default passing score
    
    def get_test_progress(self, user_progress_id, test_type=None):
        """
        Get user's test progress
        
        Args:
            user_progress_id: The user progress ID
            test_type: Optional specific test type
        
        Returns:
            TestProgress object(s) or None
        """
        try:
            if test_type:
                return TestProgress.query.filter_by(
                    user_progress_id=user_progress_id,
                    test_type=test_type
                ).first()
            else:
                return TestProgress.query.filter_by(
                    user_progress_id=user_progress_id
                ).order_by(TestProgress.test_number).all()
        except Exception as e:
            print(f"Error getting test progress: {e}")
            return None if test_type else []
    
    def is_test_unlocked(self, user_progress_id, test_type):
        """
        Check if a test is unlocked based on completed topics
        
        Args:
            user_progress_id: The user progress ID
            test_type: The test type to check
        
        Returns:
            Tuple (unlocked: bool, message: str)
        """
        try:
            # Get completed topics
            completed_topics = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id,
                completed=True
            ).all()
            
            completed_numbers = [t.topic_number for t in completed_topics]
            
            # Define requirements for each test
            requirements = {
                'checkpoint_1': {
                    'topics': [1, 2, 3, 4],
                    'message': 'Complete topics 1-4 to unlock Test 1'
                },
                'checkpoint_2': {
                    'topics': [5, 6, 7, 8],
                    'message': 'Complete topics 5-8 to unlock Test 2',
                    'prerequisite_test': 'checkpoint_1'
                },
                'final': {
                    'topics': [9, 10, 11, 12],
                    'message': 'Complete topics 9-12 to unlock Final Test',
                    'prerequisite_test': 'checkpoint_2'
                }
            }
            
            if test_type not in requirements:
                return False, 'Invalid test type'
            
            req = requirements[test_type]
            
            # Check prerequisite test if exists
            if 'prerequisite_test' in req:
                prereq_test = self.get_test_progress(user_progress_id, req['prerequisite_test'])
                if not prereq_test or not prereq_test.passed:
                    return False, f'Must pass {req["prerequisite_test"]} first'
            
            # Check required topics
            topics_complete = all(topic in completed_numbers for topic in req['topics'])
            
            if topics_complete:
                return True, 'Test is unlocked'
            else:
                missing = [t for t in req['topics'] if t not in completed_numbers]
                return False, f'{req["message"]} (Missing topics: {missing})'
            
        except Exception as e:
            print(f"Error checking test unlock: {e}")
            return False, 'Error checking test status'
    
    def record_test_attempt(self, user_progress_id, test_type, score):
        """
        Record a test attempt and check if passed
        
        Args:
            user_progress_id: The user progress ID
            test_type: The test type
            score: The test score (0-100)
        
        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            # Check if test is unlocked
            unlocked, message = self.is_test_unlocked(user_progress_id, test_type)
            if not unlocked:
                return False, {'error': message}
            
            # Get or create test progress
            test_progress = self.get_test_progress(user_progress_id, test_type)
            
            if not test_progress:
                # Should have been created during initialization
                return False, {'error': 'Test progress not found'}
            
            # Record the attempt
            passed = test_progress.record_attempt(score, self.passing_threshold)
            self.db.session.commit()
            
            result = {
                'passed': passed,
                'score': score,
                'attempts': test_progress.attempts,
                'passing_threshold': self.passing_threshold
            }
            
            # If final test passed, handle level advancement
            if passed and test_type == 'final':
                advancement_result = self._handle_level_advancement(user_progress_id)
                result['advancement'] = advancement_result
            
            return True, result
            
        except Exception as e:
            self.db.session.rollback()
            print(f"Error recording test attempt: {e}")
            return False, {'error': 'Failed to record test attempt'}
    
    def _handle_level_advancement(self, user_progress_id):
        """
        Handle advancement to next level after passing final test
        
        Args:
            user_progress_id: The user progress ID
        
        Returns:
            Dict with advancement info
        """
        try:
            # Get user progress
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return {'error': 'User progress not found'}
            
            current_level = user_progress.current_level
            
            # Define level progression
            level_progression = {
                'A1': 'A2',
                'A2': 'B1',
                'B1': 'B2',
                'B2': None  # Max level
            }
            
            next_level = level_progression.get(current_level)
            
            if next_level:
                # Update user's level
                user_progress.update_progress(new_level=next_level, progress_in_level=0)
                self.db.session.commit()
                
                # Initialize topics for new level (would be done by TopicManager)
                from topics.topic_manager import TopicManager
                topic_mgr = TopicManager()
                topic_mgr.initialize_user_topics(user_progress_id, next_level)
                
                return {
                    'advanced': True,
                    'from_level': current_level,
                    'to_level': next_level,
                    'message': f'Congratulations! Advanced from {current_level} to {next_level}'
                }
            else:
                return {
                    'advanced': False,
                    'message': 'Congratulations! You have completed the highest level!'
                }
                
        except Exception as e:
            print(f"Error handling level advancement: {e}")
            return {'error': 'Failed to advance level'}
    
    def get_test_status_summary(self, user_progress_id):
        """
        Get summary of all test statuses for a user
        
        Args:
            user_progress_id: The user progress ID
        
        Returns:
            Dict with test status summary
        """
        try:
            tests = self.get_test_progress(user_progress_id)
            
            summary = {
                'checkpoint_1': None,
                'checkpoint_2': None,
                'final': None
            }
            
            for test in tests:
                unlocked, unlock_message = self.is_test_unlocked(user_progress_id, test.test_type)
                
                summary[test.test_type] = {
                    'passed': test.passed,
                    'score': test.score,
                    'attempts': test.attempts,
                    'unlocked': unlocked,
                    'unlock_message': unlock_message,
                    'status': test.get_status()
                }
            
            return summary
            
        except Exception as e:
            print(f"Error getting test status summary: {e}")
            return {}
    
    def reset_test(self, user_progress_id, test_type):
        """
        Reset a test (mainly for testing purposes)
        
        Args:
            user_progress_id: The user progress ID
            test_type: The test type to reset
        
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            test = self.get_test_progress(user_progress_id, test_type)
            
            if test:
                test.reset_test()
                self.db.session.commit()
                return True, f'Test {test_type} reset successfully'
            else:
                return False, 'Test not found'
                
        except Exception as e:
            self.db.session.rollback()
            print(f"Error resetting test: {e}")
            return False, 'Failed to reset test'

    def check_and_unlock_test(self, user_progress_id):
        """
        Check if any test should be unlocked after topic completion

        Args:
            user_progress_id: The user progress ID

        Returns:
            Dict with test unlock info or None
        """
        try:
            # Get completed topics
            completed_topics = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id,
                completed=True
            ).all()

            completed_numbers = set(t.topic_number for t in completed_topics)

            # Check each test type
            tests_to_check = [
                ('checkpoint_1', {1, 2, 3, 4}, 'Test 1 is now available'),
                ('checkpoint_2', {5, 6, 7, 8}, 'Test 2 is now available'),
                ('final', {9, 10, 11, 12}, 'Final Test is now available')
            ]

            for test_type, required_topics, message in tests_to_check:
                # Check if all required topics are completed
                if required_topics.issubset(completed_numbers):
                    # Check if test is not yet passed
                    test_progress = self.get_test_progress(user_progress_id, test_type)
                    if test_progress and not test_progress.passed:
                        # Check prerequisites
                        if test_type == 'checkpoint_2':
                            prereq = self.get_test_progress(user_progress_id, 'checkpoint_1')
                            if not prereq or not prereq.passed:
                                continue
                        elif test_type == 'final':
                            prereq = self.get_test_progress(user_progress_id, 'checkpoint_2')
                            if not prereq or not prereq.passed:
                                continue

                        # Test is newly unlocked
                        return {
                            'test_type': test_type,
                            'test_number': test_progress.test_number,
                            'message': message,
                            'unlocked': True
                        }

            return None

        except Exception as e:
            print(f"Error checking test unlock: {e}")
            return None

    def get_current_test_requirement(self, user_progress_id):
        """
        Get the current test that needs to be taken

        Args:
            user_progress_id: The user progress ID

        Returns:
            Dict with test info or None
        """
        try:
            # Check tests in order
            tests = self.get_test_progress(user_progress_id)

            for test in tests:
                # Check if test is unlocked but not passed
                unlocked, message = self.is_test_unlocked(user_progress_id, test.test_type)

                if unlocked and not test.passed:
                    return {
                        'test_type': test.test_type,
                        'test_number': test.test_number,
                        'attempts': test.attempts,
                        'last_score': test.score,
                        'message': f'Complete {test.test_type.replace("_", " ").title()} to continue'
                    }

            return None

        except Exception as e:
            print(f"Error getting current test requirement: {e}")
            return None

    def can_proceed_to_topic(self, user_progress_id, topic_number):
        """
        Check if user can proceed to a specific topic (not blocked by test)

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic to check

        Returns:
            Tuple (can_proceed: bool, blocking_test: str or None)
        """
        try:
            # Topics 5-8 require checkpoint_1
            if topic_number in [5, 6, 7, 8]:
                test = self.get_test_progress(user_progress_id, 'checkpoint_1')
                if not test or not test.passed:
                    # Check if topics 1-4 are complete
                    topics_complete = TopicProgress.query.filter_by(
                        user_progress_id=user_progress_id,
                        completed=True
                    ).filter(TopicProgress.topic_number.in_([1, 2, 3, 4])).count() == 4

                    if topics_complete:
                        return False, 'checkpoint_1'

            # Topics 9-12 require checkpoint_2
            elif topic_number in [9, 10, 11, 12]:
                test = self.get_test_progress(user_progress_id, 'checkpoint_2')
                if not test or not test.passed:
                    # Check if topics 5-8 are complete
                    topics_complete = TopicProgress.query.filter_by(
                        user_progress_id=user_progress_id,
                        completed=True
                    ).filter(TopicProgress.topic_number.in_([5, 6, 7, 8])).count() == 4

                    if topics_complete:
                        return False, 'checkpoint_2'

            return True, None

        except Exception as e:
            print(f"Error checking topic proceed: {e}")
            return False, 'error'