# Progress Manager for Spralingua
# Handles all database operations for language learning progress

from database import db
from models.user_progress import UserProgress
from sqlalchemy.exc import IntegrityError

class ProgressManager:
    """Manages user progress tracking for language pairs"""
    
    def __init__(self):
        """Initialize the ProgressManager"""
        self.db = db
    
    def get_user_progress(self, user_id, input_language=None, target_language=None):
        """
        Get user's progress for a specific language pair or most recent
        
        Args:
            user_id: The user's ID
            input_language: Optional specific input language
            target_language: Optional specific target language
        
        Returns:
            UserProgress object or None
        """
        try:
            query = UserProgress.query.filter_by(user_id=user_id)
            
            if input_language and target_language:
                # Get specific language pair
                progress = query.filter_by(
                    input_language=input_language.lower(),
                    target_language=target_language.lower()
                ).first()
            else:
                # Get most recently accessed progress
                progress = query.order_by(UserProgress.last_accessed.desc()).first()
            
            return progress
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return None
    
    def get_or_create_progress(self, user_id, input_language, target_language):
        """
        Get existing progress or create new one if it doesn't exist

        Args:
            user_id: The user's ID
            input_language: The input language
            target_language: The target language

        Returns:
            UserProgress object or None
        """
        try:
            # First try to get existing progress
            existing = self.get_user_progress(user_id, input_language, target_language)

            if existing:
                return existing

            # Create new progress if doesn't exist
            new_progress = UserProgress(
                user_id=user_id,
                input_language=input_language.lower(),
                target_language=target_language.lower(),
                current_level='A1'  # Default to A1 for new progress
            )

            self.db.session.add(new_progress)
            self.db.session.commit()

            # Initialize topics and tests for the new progress
            # Import here to avoid circular import
            from topics.topic_manager import TopicManager
            topic_mgr = TopicManager()
            success, message = topic_mgr.initialize_user_topics(new_progress.id, 'A1')

            if not success:
                print(f"[WARNING] Failed to initialize topics: {message}")

            return new_progress

        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] get_or_create_progress failed: {e}")
            return None

    def save_progress(self, user_id, input_language, target_language, current_level):
        """
        Save or update user's progress for a language pair
        
        Args:
            user_id: The user's ID
            input_language: The input language
            target_language: The target language
            current_level: The current level (A1, A2, B1, B2)
        
        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            # Check if progress already exists for this language pair
            existing = self.get_user_progress(user_id, input_language, target_language)
            
            if existing:
                # Update existing progress
                existing.update_progress(new_level=current_level)
                self.db.session.commit()
                
                return True, {
                    'message': 'Progress updated successfully',
                    'progress': existing.to_dict()
                }
            else:
                # Create new progress record
                new_progress = UserProgress(
                    user_id=user_id,
                    input_language=input_language,
                    target_language=target_language,
                    current_level=current_level
                )
                
                self.db.session.add(new_progress)
                self.db.session.commit()
                
                return True, {
                    'message': 'Progress saved successfully',
                    'progress': new_progress.to_dict()
                }
                
        except IntegrityError as e:
            self.db.session.rollback()
            return False, {'error': 'Database integrity error'}
        except Exception as e:
            self.db.session.rollback()
            print(f"Error saving progress: {e}")
            return False, {'error': 'Failed to save progress'}
    
    def get_all_user_pairs(self, user_id):
        """
        Get all language pairs for a user
        
        Args:
            user_id: The user's ID
        
        Returns:
            List of UserProgress objects
        """
        try:
            progress_records = UserProgress.query.filter_by(user_id=user_id)\
                .order_by(UserProgress.last_accessed.desc()).all()
            return progress_records
        except Exception as e:
            print(f"Error getting all user pairs: {e}")
            return []
    
    def delete_progress(self, user_id, input_language, target_language):
        """
        Delete a specific progress record
        
        Args:
            user_id: The user's ID
            input_language: The input language
            target_language: The target language
        
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            progress = self.get_user_progress(user_id, input_language, target_language)
            
            if progress:
                self.db.session.delete(progress)
                self.db.session.commit()
                return True, 'Progress deleted successfully'
            else:
                return False, 'Progress record not found'
                
        except Exception as e:
            self.db.session.rollback()
            print(f"Error deleting progress: {e}")
            return False, 'Failed to delete progress'
    
    def save_progress_with_initialization(self, user_id, input_language, target_language, current_level):
        """
        Save or update user's progress AND ensure topics are initialized.
        Combines the behavior of save_progress() with topic initialization.

        Args:
            user_id: The user's ID
            input_language: The input language
            target_language: The target language
            current_level: The current level (A1, A2, B1, B2)

        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            # Check if progress already exists for this language pair
            existing = self.get_user_progress(user_id, input_language, target_language)

            if existing:
                # ALWAYS update last_accessed when user selects this language pair from dashboard
                from datetime import datetime
                existing.last_accessed = datetime.utcnow()

                # Update existing progress level if different
                if existing.current_level != current_level:
                    existing.update_progress(new_level=current_level)
                    print(f"[INFO] Updated level from {existing.current_level} to {current_level}")

                # Commit the changes (includes last_accessed update even if level didn't change)
                self.db.session.commit()

                # Check if topics are initialized for the CURRENT LEVEL
                from topics.topic_manager import TopicManager
                from models.topic_progress import TopicProgress

                topic_mgr = TopicManager()
                # Check specifically for this level's topics
                topic_count = TopicProgress.query.filter_by(
                    user_progress_id=existing.id,
                    level=current_level.upper()
                ).count()

                if topic_count == 0:
                    print(f"[WARNING] No topics found for level {current_level} in progress {existing.id}, initializing...")
                    success, message = topic_mgr.initialize_user_topics(existing.id, current_level)
                    if not success:
                        print(f"[ERROR] Failed to initialize topics: {message}")
                    else:
                        print(f"[SUCCESS] Initialized topics for existing user")

                return True, {
                    'message': 'Progress updated successfully',
                    'progress': existing.to_dict()
                }
            else:
                # Create new progress record
                new_progress = UserProgress(
                    user_id=user_id,
                    input_language=input_language.lower(),
                    target_language=target_language.lower(),
                    current_level=current_level
                )

                self.db.session.add(new_progress)
                self.db.session.commit()

                # Initialize topics for the new progress
                from topics.topic_manager import TopicManager
                topic_mgr = TopicManager()
                success, message = topic_mgr.initialize_user_topics(new_progress.id, current_level)

                if not success:
                    print(f"[ERROR] Failed to initialize topics for new progress: {message}")
                else:
                    print(f"[SUCCESS] Created progress and initialized topics")

                return True, {
                    'message': 'Progress saved successfully with topics initialized',
                    'progress': new_progress.to_dict()
                }

        except IntegrityError as e:
            self.db.session.rollback()
            print(f"[ERROR] Database integrity error: {e}")
            return False, {'error': 'Progress already exists for this language pair'}
        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] save_progress_with_initialization failed: {e}")
            return False, {'error': 'Failed to save progress'}

    def update_progress_in_level(self, user_id, input_language, target_language, progress_percentage):
        """
        Update the progress percentage within a level
        
        Args:
            user_id: The user's ID
            input_language: The input language
            target_language: The target language
            progress_percentage: Progress within the level (0-100)
        
        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            progress = self.get_user_progress(user_id, input_language, target_language)
            
            if progress:
                progress.update_progress(progress_in_level=min(100, max(0, progress_percentage)))
                self.db.session.commit()
                
                return True, {
                    'message': 'Progress updated',
                    'progress': progress.to_dict()
                }
            else:
                return False, {'error': 'Progress record not found'}
                
        except Exception as e:
            self.db.session.rollback()
            print(f"Error updating progress in level: {e}")
            return False, {'error': 'Failed to update progress'}