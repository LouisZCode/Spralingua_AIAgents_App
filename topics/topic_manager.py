# Topic Manager for Spralingua
# Handles topic progression and tracking

from database import db
from models.topic_definition import TopicDefinition
from models.topic_progress import TopicProgress
from models.test_progress import TestProgress
from models.user_progress import UserProgress
from sqlalchemy.exc import IntegrityError

class TopicManager:
    """Manages topic progression and tracking for language learning"""
    
    def __init__(self):
        """Initialize the TopicManager"""
        self.db = db
    
    def get_topic_definition(self, level, topic_number):
        """
        Get a specific topic definition
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
        
        Returns:
            TopicDefinition object or None
        """
        try:
            topic = TopicDefinition.query.filter_by(
                level=level.upper(),
                topic_number=topic_number
            ).first()
            return topic
        except Exception as e:
            print(f"Error getting topic definition: {e}")
            return None
    
    def get_all_topics_for_level(self, level):
        """
        Get all topic definitions for a level
        
        Args:
            level: The level (A1, A2, B1, B2)
        
        Returns:
            List of TopicDefinition objects
        """
        try:
            topics = TopicDefinition.query.filter_by(
                level=level.upper()
            ).order_by(TopicDefinition.topic_number).all()
            return topics
        except Exception as e:
            print(f"Error getting topics for level: {e}")
            return []
    
    def get_user_topic_progress(self, user_progress_id, level, topic_number=None):
        """
        Get user's progress for a specific topic or all topics

        Args:
            user_progress_id: The user progress ID
            level: The level (A1, A2, B1, B2)
            topic_number: Optional specific topic number

        Returns:
            TopicProgress object(s) or None
        """
        try:
            if topic_number:
                return TopicProgress.query.filter_by(
                    user_progress_id=user_progress_id,
                    level=level.upper(),
                    topic_number=topic_number
                ).first()
            else:
                return TopicProgress.query.filter_by(
                    user_progress_id=user_progress_id,
                    level=level.upper()
                ).order_by(TopicProgress.topic_number).all()
        except Exception as e:
            print(f"Error getting user topic progress: {e}")
            return None if topic_number else []

    def ensure_topic_progress_exists(self, user_progress_id, level, topic_number):
        """
        Ensure topic progress record exists, create if missing (resilience)

        Args:
            user_progress_id: The user progress ID
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number

        Returns:
            TopicProgress object (existing or newly created)
        """
        try:
            # First check if it exists
            existing = self.get_user_topic_progress(user_progress_id, level, topic_number)
            if existing:
                return existing

            print(f"[WARNING] Topic progress missing for topic {topic_number}, creating...")

            # Create it if missing
            new_progress = TopicProgress(
                user_progress_id=user_progress_id,
                level=level,
                topic_number=topic_number,
                total_exercises=5  # Default number of exercises
            )
            self.db.session.add(new_progress)
            self.db.session.commit()

            print(f"[SUCCESS] Created missing topic progress for topic {topic_number}")
            return new_progress

        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] Failed to ensure topic progress: {e}")
            return None
    
    def initialize_user_topics(self, user_progress_id, level):
        """
        Initialize all topic progress records for a user starting a level
        
        Args:
            user_progress_id: The user progress ID
            level: The level to initialize
        
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            # Get all topics for the level
            topics = self.get_all_topics_for_level(level)
            
            if not topics:
                return False, f"No topics found for level {level}"
            
            # Create progress records for each topic
            for topic in topics:
                # Check if progress already exists
                existing = TopicProgress.query.filter_by(
                    user_progress_id=user_progress_id,
                    level=level.upper(),
                    topic_number=topic.topic_number
                ).first()
                
                if not existing:
                    # Count exercises for this topic (for now, set a default)
                    # In future, this would count actual TopicExercise records
                    total_exercises = 5  # Default number of exercises per topic
                    
                    progress = TopicProgress(
                        user_progress_id=user_progress_id,
                        level=level,
                        topic_number=topic.topic_number,
                        total_exercises=total_exercises
                    )
                    self.db.session.add(progress)
            
            # Initialize test progress records
            test_types = [
                ('checkpoint_1', 1),
                ('checkpoint_2', 2),
                ('final', 3)
            ]
            
            for test_type, test_number in test_types:
                existing_test = TestProgress.query.filter_by(
                    user_progress_id=user_progress_id,
                    test_type=test_type
                ).first()
                
                if not existing_test:
                    test_progress = TestProgress(
                        user_progress_id=user_progress_id,
                        test_type=test_type,
                        test_number=test_number
                    )
                    self.db.session.add(test_progress)
            
            self.db.session.commit()
            return True, f"Initialized topics for level {level}"
            
        except Exception as e:
            self.db.session.rollback()
            print(f"Error initializing user topics: {e}")
            return False, f"Failed to initialize topics: {str(e)}"
    
    def get_current_topic(self, user_progress_id):
        """
        Get the current topic a user should be working on

        Args:
            user_progress_id: The user progress ID

        Returns:
            Dict with current topic info or None
        """
        try:
            # Get user progress to determine level
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return None

            # Get all topic progress
            all_progress = self.get_user_topic_progress(user_progress_id, user_progress.current_level)
            
            if not all_progress:
                return None
            
            # Get test progress
            tests = TestProgress.query.filter_by(
                user_progress_id=user_progress_id
            ).all()
            
            # Check for test gates
            checkpoint_1 = next((t for t in tests if t.test_type == 'checkpoint_1'), None)
            checkpoint_2 = next((t for t in tests if t.test_type == 'checkpoint_2'), None)
            
            # Find the first incomplete topic that's not gated
            for progress in all_progress:
                topic_num = progress.topic_number
                
                # Check if topic is gated by a test
                if topic_num in [5, 6, 7, 8] and checkpoint_1 and not checkpoint_1.passed:
                    # Need to pass checkpoint 1 first
                    completed_1_to_4 = all(
                        p.completed for p in all_progress if p.topic_number in [1, 2, 3, 4]
                    )
                    if completed_1_to_4:
                        return {
                            'type': 'test',
                            'test_type': 'checkpoint_1',
                            'test_number': 1,
                            'message': 'Complete Test 1 to unlock topics 5-8'
                        }
                    continue
                    
                elif topic_num in [9, 10, 11, 12] and checkpoint_2 and not checkpoint_2.passed:
                    # Need to pass checkpoint 2 first
                    completed_5_to_8 = all(
                        p.completed for p in all_progress if p.topic_number in [5, 6, 7, 8]
                    )
                    if completed_5_to_8:
                        return {
                            'type': 'test',
                            'test_type': 'checkpoint_2',
                            'test_number': 2,
                            'message': 'Complete Test 2 to unlock topics 9-12'
                        }
                    continue
                
                # If topic is not completed and not gated, it's current
                if not progress.completed:
                    # Get the user's level from UserProgress
                    user_prog = UserProgress.query.get(user_progress_id)
                    if user_prog:
                        topic_def = self.get_topic_definition(user_prog.current_level, topic_num)
                        if topic_def:
                            return {
                                'type': 'topic',
                                'topic_number': topic_num,
                                'title_key': topic_def.title_key,
                                'progress': progress.to_dict(),
                                'definition': topic_def.to_dict()
                            }
            
            # All topics completed, check for final test
            final_test = next((t for t in tests if t.test_type == 'final'), None)
            if final_test and not final_test.passed:
                return {
                    'type': 'test',
                    'test_type': 'final',
                    'test_number': 3,
                    'message': 'Complete Final Test to advance to next level'
                }
            
            # Everything completed!
            return {
                'type': 'completed',
                'message': 'Level completed! Ready to advance.'
            }
            
        except Exception as e:
            print(f"Error getting current topic: {e}")
            return None
    
    def complete_topic_exercise(self, user_progress_id, level, topic_number):
        """
        Mark an exercise as completed for a topic

        Args:
            user_progress_id: The user progress ID
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number

        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            progress = self.get_user_topic_progress(user_progress_id, level, topic_number)
            
            if not progress:
                return False, {'error': 'Topic progress not found'}
            
            # Complete an exercise
            topic_completed = progress.complete_exercise()
            self.db.session.commit()
            
            result = {
                'exercises_completed': progress.exercises_completed,
                'total_exercises': progress.total_exercises,
                'topic_completed': topic_completed,
                'progress_percentage': progress.get_progress_percentage()
            }
            
            return True, result
            
        except Exception as e:
            self.db.session.rollback()
            print(f"Error completing topic exercise: {e}")
            return False, {'error': 'Failed to complete exercise'}
    
    def get_completed_topics(self, user_progress_id):
        """
        Get list of completed topic numbers for a user
        
        Args:
            user_progress_id: The user progress ID
        
        Returns:
            List of completed topic numbers
        """
        try:
            completed = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id,
                completed=True
            ).all()
            
            return [p.topic_number for p in completed]
            
        except Exception as e:
            print(f"Error getting completed topics: {e}")
            return []
    
    # New enhanced methods for database-driven prompts
    
    def get_topic_word_limit(self, level, topic_number):
        """
        Get word limit for a specific topic (override or level default)
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
        
        Returns:
            Word limit integer
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if topic and topic.word_limit:
                # Topic has specific word limit override
                return topic.word_limit
            
            # Fall back to level default
            from level_rules.level_rules_manager import LevelRulesManager
            level_mgr = LevelRulesManager()
            return level_mgr.get_word_limit(level)
            
        except Exception as e:
            print(f"Error getting topic word limit: {e}")
            # Ultimate fallback
            return 40 if level.upper() == 'A1' else 50
    
    def get_opening_phrase(self, level, topic_number, language):
        """
        Get localized opening phrase for a topic
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
            language: Target language (german, spanish, portuguese, english)
        
        Returns:
            Opening phrase string or None
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if topic and topic.opening_phrases:
                return topic.opening_phrases.get(language.lower())
            return None
            
        except Exception as e:
            print(f"Error getting opening phrase: {e}")
            return None
    
    def get_conversation_flow(self, level, topic_number):
        """
        Get structured conversation flow for a topic
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
        
        Returns:
            List of conversation steps or empty list
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if topic and topic.conversation_flow:
                return topic.conversation_flow
            return []
            
        except Exception as e:
            print(f"Error getting conversation flow: {e}")
            return []
    
    def get_required_vocabulary(self, level, topic_number):
        """
        Get required vocabulary list for a topic
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
        
        Returns:
            List of vocabulary items or empty list
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if topic and topic.required_vocabulary:
                return topic.required_vocabulary
            return []
            
        except Exception as e:
            print(f"Error getting required vocabulary: {e}")
            return []
    
    def get_topic_specific_rules(self, level, topic_number):
        """
        Get topic-specific rules and guidance
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
        
        Returns:
            Rules text string or None
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if topic and topic.topic_specific_rules:
                return topic.topic_specific_rules
            return None
            
        except Exception as e:
            print(f"Error getting topic specific rules: {e}")
            return None
    
    def get_number_of_exchanges(self, level, topic_number):
        """
        Get number of exchanges for a topic conversation
        
        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-12)
        
        Returns:
            Number of exchanges integer
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if topic and topic.number_of_exchanges:
                return topic.number_of_exchanges
            return 5  # Default
            
        except Exception as e:
            print(f"Error getting number of exchanges: {e}")
            return 5

    def get_scenario_template(self, level, topic_number, language='english'):
        """
        Get scenario template for a topic in specified language

        Args:
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number (1-16)
            language: The language for the scenario (english, spanish, german, portuguese)

        Returns:
            Scenario template string or None
        """
        try:
            topic = self.get_topic_definition(level, topic_number)
            if not topic:
                return None

            # Map language to appropriate database column
            language_lower = language.lower()

            if language_lower == 'spanish' and topic.scenario_spanish:
                return topic.scenario_spanish
            elif language_lower == 'german' and topic.scenario_german:
                return topic.scenario_german
            elif language_lower == 'portuguese' and topic.scenario_portuguese:
                return topic.scenario_portuguese
            else:
                # Default to English (scenario_template column)
                return topic.scenario_template

        except Exception as e:
            print(f"Error getting scenario template: {e}")
            return None

    def mark_topic_complete(self, user_progress_id, level, topic_number):
        """
        Mark a topic as complete and update current_topic

        Args:
            user_progress_id: The user progress ID
            level: The level (A1, A2, B1, B2)
            topic_number: The topic number to complete

        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            # Get the topic progress (with auto-create if missing for resilience)
            topic_progress = self.ensure_topic_progress_exists(user_progress_id, level, topic_number)
            if not topic_progress:
                return False, {'error': f'Topic {topic_number} progress could not be created'}

            # Mark as complete
            if not topic_progress.completed:
                topic_progress.mark_complete()

            # Get user progress to update current topic
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return False, {'error': 'User progress not found'}

            # Determine next topic
            next_topic = self._determine_next_topic(user_progress_id, topic_number)

            # Update current_topic if we have a next topic
            if next_topic and next_topic['type'] == 'topic':
                user_progress.current_topic = next_topic['topic_number']
            elif next_topic and next_topic['type'] == 'test':
                # Keep current topic but indicate test is needed
                pass
            elif next_topic and next_topic['type'] == 'completed':
                # Level completed - keep at last topic
                user_progress.current_topic = 16

            self.db.session.commit()

            return True, {
                'topic_completed': True,
                'current_topic': user_progress.current_topic,
                'next_item': next_topic
            }

        except Exception as e:
            self.db.session.rollback()
            print(f"Error marking topic complete: {e}")
            return False, {'error': str(e)}

    def _determine_next_topic(self, user_progress_id, completed_topic_number):
        """
        Determine what comes next after completing a topic

        In the 16-topic system, tests are integrated as regular topics at positions 4, 8, 12, 16

        Args:
            user_progress_id: The user progress ID
            completed_topic_number: The topic that was just completed

        Returns:
            Dict with next item info (topic or completed)
        """
        try:
            # Simply advance to the next sequential topic
            if completed_topic_number < 16:
                next_topic_num = completed_topic_number + 1

                # Get user progress for level
                user_prog = UserProgress.query.get(user_progress_id)
                if user_prog:
                    # Get topic definition for the next topic
                    topic_def = self.get_topic_definition(user_prog.current_level, next_topic_num)
                    if topic_def:
                        return {
                            'type': 'topic',
                            'topic_number': next_topic_num,
                            'title_key': topic_def.title_key
                        }

            # Check if level is completed (all 16 topics done)
            elif completed_topic_number == 16:
                user_prog = UserProgress.query.get(user_progress_id)
                if user_prog:
                    # All 16 topics completed - level is done
                    return {
                        'type': 'completed',
                        'message': 'Level completed! Ready to advance to next level.'
                    }

            return None

        except Exception as e:
            print(f"Error determining next topic: {e}")
            return None

    def check_completion_popup_needed(self, user_progress_id):
        """
        Check if a completion popup should be shown for any completed topic

        Args:
            user_progress_id: The user progress ID

        Returns:
            Dict with popup info or None if no popup needed
        """
        try:
            # Get user progress for context
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return None

            # Look for ANY completed topic that hasn't shown its popup yet
            # Get the earliest one (lowest topic number) to show in order
            completed_without_popup = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id,
                completed=True,
                has_seen_completion_popup=False
            ).order_by(TopicProgress.topic_number).first()

            if completed_without_popup:
                completed_topic_num = completed_without_popup.topic_number

                # Determine what comes after this completed topic
                next_item = self._determine_next_topic(user_progress_id, completed_topic_num)

                if next_item:
                    print(f"[INFO] Popup needed for completed Topic {completed_topic_num}")
                    return {
                        'show_popup': True,
                        'completed_topic': completed_topic_num,
                        'next_item': next_item,
                        'is_test': next_item['type'] == 'test'
                    }

            return None

        except Exception as e:
            print(f"[ERROR] Checking completion popup: {e}")
            return None

    def mark_popup_seen(self, user_progress_id, topic_number):
        """
        Mark that the completion popup has been shown for a topic

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic number

        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            # Get user progress for level
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return False, 'User progress not found'

            topic_progress = self.get_user_topic_progress(user_progress_id, user_progress.current_level, topic_number)
            if not topic_progress:
                return False, 'Topic progress not found'

            # Check if the attribute exists (for existing records before migration)
            if not hasattr(topic_progress, 'has_seen_completion_popup'):
                print(f"[WARNING] Topic progress {topic_number} missing has_seen_completion_popup field")
                return True, 'Field not available - skipping'

            topic_progress.mark_popup_seen()
            self.db.session.commit()
            return True, 'Popup marked as seen'

        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] Marking popup seen: {e}")
            return False, str(e)

    def navigate_to_topic(self, user_progress_id, new_topic_number):
        """
        Navigate to a different topic (used when clicking on progress circles)

        Args:
            user_progress_id: The user progress ID
            new_topic_number: The topic to navigate to

        Returns:
            Tuple (success: bool, result: dict)
        """
        try:
            # Check if user can access this topic
            can_access, reason = self.can_access_topic(user_progress_id, new_topic_number)
            if not can_access:
                return False, {'error': reason}

            # Get user progress
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return False, {'error': 'User progress not found'}

            # Check if user can actually access this topic based on completed topics
            all_topic_progress = self.get_user_topic_progress(user_progress_id, user_progress.current_level)
            completed_topics = [tp.topic_number for tp in all_topic_progress if tp.completed]
            max_accessible = max(completed_topics) + 1 if completed_topics else user_progress.current_topic

            # Don't allow navigation to locked topics
            if new_topic_number > max_accessible:
                return False, {'error': f'Topic {new_topic_number} is locked. Complete earlier topics first.'}

            # Only update current_topic if moving forward (to track progression)
            # Allow backward navigation without changing current_topic
            if new_topic_number > user_progress.current_topic:
                user_progress.current_topic = new_topic_number

            self.db.session.commit()

            return True, {
                'current_topic': user_progress.current_topic,
                'navigated_to': new_topic_number,
                'message': f'Navigated to Topic {new_topic_number}'
            }

        except Exception as e:
            self.db.session.rollback()
            print(f"[ERROR] Navigating to topic: {e}")
            return False, {'error': str(e)}

    def can_access_topic(self, user_progress_id, topic_number):
        """
        Check if a user can access a specific topic

        Args:
            user_progress_id: The user progress ID
            topic_number: The topic to check access for

        Returns:
            Tuple (can_access: bool, reason: str)
        """
        try:
            # Get user progress for level
            user_progress = UserProgress.query.get(user_progress_id)
            if not user_progress:
                return False, "User progress not found"

            # Get all progress
            all_progress = self.get_user_topic_progress(user_progress_id, user_progress.current_level)
            tests = TestProgress.query.filter_by(user_progress_id=user_progress_id).all()

            # Topic 1 is always accessible
            if topic_number == 1:
                return True, "First topic is always accessible"

            # Check if previous topic is completed
            prev_topic = next((p for p in all_progress if p.topic_number == topic_number - 1), None)
            if prev_topic and not prev_topic.completed:
                return False, f"Complete Topic {topic_number - 1} first"

            # In 16-topic system, no test gates - just sequential progression
            return True, "Topic is accessible"

        except Exception as e:
            print(f"Error checking topic access: {e}")
            return False, str(e)