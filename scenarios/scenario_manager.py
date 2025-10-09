# Scenario Manager for Spralingua
# Handles scenario template processing and translation

from typing import Dict, Optional, Tuple
from topics.topic_manager import TopicManager
from progress.progress_manager import ProgressManager

class ScenarioManager:
    """Manages scenario generation and translation for conversation practice"""

    def __init__(self):
        """Initialize the ScenarioManager with required managers"""
        self.topic_manager = TopicManager()
        self.progress_manager = ProgressManager()

        # Language name translations
        # Used to translate the {target_language} placeholder in scenarios
        # Each language has translations for all target languages
        self.language_translations = {
            'english': {
                'german': 'German',
                'spanish': 'Spanish',
                'portuguese': 'Portuguese',
                'english': 'English'
            },
            'german': {
                'german': 'Deutsch',
                'spanish': 'Spanisch',
                'portuguese': 'Portugiesisch',
                'english': 'Englisch'
            },
            'spanish': {
                'german': 'Alemán',
                'spanish': 'Español',
                'portuguese': 'Portugués',
                'english': 'Inglés'
            },
            'portuguese': {
                'german': 'Alemão',
                'spanish': 'Espanhol',
                'portuguese': 'Português',
                'english': 'Inglês'
            }
        }

    def get_scenario_for_user(self, user_id: int, character: str = 'harry', topic_override: int = None) -> Tuple[str, Dict]:
        """
        Get a translated scenario for the user's current topic and language pair

        Args:
            user_id: The user's ID
            character: The character name (default: 'harry')

        Returns:
            Tuple of (translated_scenario, context_dict)
        """
        try:
            # Get user's current progress
            user_progress = self.progress_manager.get_user_progress(user_id)

            if not user_progress:
                # Return a default scenario if no progress
                return self._get_default_scenario(), {}

            # Extract user context
            input_language = user_progress.input_language.lower()
            target_language = user_progress.target_language.lower()
            level = user_progress.current_level

            # Use topic override if provided, otherwise determine current topic
            if topic_override:
                topic_number = topic_override
                print(f"[INFO] ScenarioManager: Using topic override: Topic {topic_override}")
            else:
                # Determine current topic (next uncompleted)
                topic_number = self._determine_current_topic(user_progress.id, level)

            # Get scenario template from database in user's native language
            print(f"[DEBUG] ScenarioManager: Fetching scenario for level={level}, topic={topic_number}, language={input_language}")
            scenario_template = self.topic_manager.get_scenario_template(
                level, topic_number, language=input_language
            )
            print(f"[DEBUG] ScenarioManager: Scenario template received: {'YES' if scenario_template else 'NO (None)'}")

            if not scenario_template:
                # No scenario for this topic yet, use default
                print(f"[WARNING] ScenarioManager: No scenario template found, using default fallback")
                return self._get_default_scenario_for_topic(
                    input_language, target_language, level, topic_number
                ), {
                    'level': level,
                    'topic_number': topic_number,
                    'input_language': input_language,
                    'target_language': target_language
                }

            # Process the scenario template (only replace placeholder)
            translated_scenario = self._translate_scenario(
                scenario_template,
                input_language,
                target_language
            )

            # Return scenario with context
            context = {
                'level': level,
                'topic_number': topic_number,
                'input_language': input_language,
                'target_language': target_language,
                'character': character
            }

            return translated_scenario, context

        except Exception as e:
            print(f"[ERROR] ScenarioManager.get_scenario_for_user: {e}")
            return self._get_default_scenario(), {}

    def _translate_scenario(self, template: str, input_language: str, target_language: str) -> str:
        """
        Process a scenario template by replacing the {target_language} placeholder

        The template is already in the user's native language (from database),
        we just need to replace the placeholder with the translated language name.

        Args:
            template: The scenario template with {target_language} placeholder (already translated)
            input_language: User's native language
            target_language: Language they're learning

        Returns:
            Fully processed scenario with placeholder replaced
        """
        # Get translated name of target language in user's native language
        target_lang_translated = self.language_translations.get(
            input_language, {}
        ).get(target_language, target_language.capitalize())

        # Replace the placeholder
        scenario = template.replace('{target_language}', target_lang_translated)

        return scenario

    def _determine_current_topic(self, user_progress_id: int, level: str) -> int:
        """
        Determine which topic the user should practice

        Args:
            user_progress_id: User's progress ID
            level: Current level

        Returns:
            Topic number (1-12)
        """
        try:
            # Get all topic progress for this user
            from models.topic_progress import TopicProgress
            all_progress = TopicProgress.query.filter_by(
                user_progress_id=user_progress_id
            ).all()

            if not all_progress:
                # No progress yet, start with topic 1
                return 1

            # Find the first uncompleted topic
            for topic_num in range(1, 13):  # Topics 1-12
                topic_progress = next(
                    (tp for tp in all_progress if tp.topic_number == topic_num),
                    None
                )

                if not topic_progress or not topic_progress.completed:
                    return topic_num

            # All topics completed, cycle back to 1
            return 1

        except Exception as e:
            print(f"[WARNING] Could not determine current topic: {e}")
            return 1

    def _get_default_scenario(self) -> str:
        """
        Get a generic default scenario

        Returns:
            Default scenario text
        """
        return "You're about to practice a conversation. Start by greeting your conversation partner."

    def _get_default_scenario_for_topic(
        self, input_language: str, target_language: str, level: str, topic_number: int
    ) -> str:
        """
        Generate a default scenario for topics without templates yet

        Args:
            input_language: User's native language
            target_language: Language they're learning
            level: Current level
            topic_number: Topic number

        Returns:
            Generated default scenario
        """
        # Get translated language name
        target_lang_translated = self.language_translations.get(
            input_language, {}
        ).get(target_language, target_language.capitalize())

        # Create a generic scenario based on language
        if input_language == 'spanish':
            return f"Vas a practicar {target_lang_translated} en el nivel {level}, Tema {topic_number}. Comienza la conversación."
        elif input_language == 'german':
            return f"Du wirst {target_lang_translated} auf Niveau {level}, Thema {topic_number} üben. Beginne das Gespräch."
        elif input_language == 'portuguese':
            return f"Vais praticar {target_lang_translated} no nível {level}, Tópico {topic_number}. Começa a conversa."
        else:
            return f"You're going to practice {target_lang_translated} at level {level}, Topic {topic_number}. Start the conversation."