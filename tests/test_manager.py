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