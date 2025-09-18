# Email Prompt Builder for Spralingua
# Builds dynamic email exercise prompts based on language pair, level, and topic

import os
from typing import Dict, Tuple, Optional, List
from progress.progress_manager import ProgressManager
from topics.topic_manager import TopicManager
from level_rules.level_rules_manager import LevelRulesManager

class EmailPromptBuilder:
    """
    Builds personalized email exercise prompts based on user progress.
    Similar to ConversationPromptBuilder but adapted for email exercises.
    """

    def __init__(self):
        """Initialize the EmailPromptBuilder with managers"""
        self.progress_manager = ProgressManager()
        self.topic_manager = TopicManager()
        self.level_rules_manager = LevelRulesManager()

    def build_generation_prompt(self, user_id: int) -> Tuple[str, Dict]:
        """
        Build a letter generation prompt for the given user.

        Args:
            user_id: The user's ID

        Returns:
            Tuple of (prompt_string, context_dict) where context contains user data
        """
        try:
            print(f"[DEBUG] EmailPromptBuilder: Building prompt for user_id={user_id}")

            # Get user context
            user_context = self._get_user_context(user_id)

            if not user_context:
                print(f"[ERROR] EmailPromptBuilder: No user context found for user_id={user_id}")
                return None, None

            print(f"[DEBUG] EmailPromptBuilder: User context retrieved - languages: {user_context['input_language']} to {user_context['target_language']}, level={user_context['level']}")

            # Get level rules from database
            level_rules = self.level_rules_manager.get_level_rules(user_context['level'])
            print(f"[DEBUG] EmailPromptBuilder: Level rules retrieved: {bool(level_rules)}")

            # Get topic-specific parameters from database
            topic_params = self._get_topic_parameters(
                user_context['level'],
                user_context['topic_number']
            )
            print(f"[DEBUG] EmailPromptBuilder: Topic params retrieved: {bool(topic_params)}")

            # Build the letter generation prompt
            generation_prompt = self._build_letter_prompt(
                user_context,
                level_rules,
                topic_params
            )

            print(f"[DEBUG] EmailPromptBuilder: Prompt built successfully, length={len(generation_prompt) if generation_prompt else 0}")
            return generation_prompt, user_context

        except Exception as e:
            print(f"[ERROR] EmailPromptBuilder: Exception in build_generation_prompt: {e}")
            import traceback
            print(f"[ERROR] EmailPromptBuilder: Traceback: {traceback.format_exc()}")
            return None, None

    def build_evaluation_prompt(self, user_context: Dict, attempt: int,
                               original_letter: str, student_response: str,
                               first_attempt: str = None) -> str:
        """
        Build an evaluation prompt based on attempt number and language context.

        Args:
            user_context: User's language and level context
            attempt: 1 or 2 (first or second attempt)
            original_letter: The letter the student is responding to
            student_response: The student's current response
            first_attempt: The student's first attempt (for second evaluation)

        Returns:
            Evaluation prompt string
        """
        target_language = user_context['target_language']
        native_language = user_context['input_language']
        level = user_context['level']

        # Map language to instruction language for Claude
        instruction_language = self._get_instruction_language(native_language)

        if attempt == 1:
            return self._build_first_attempt_prompt(
                target_language, instruction_language, level,
                original_letter, student_response
            )
        else:
            return self._build_second_attempt_prompt(
                target_language, instruction_language, level,
                original_letter, first_attempt, student_response
            )

    def _get_user_context(self, user_id: int) -> Optional[Dict]:
        """Get user's language pair, level, and current topic"""
        try:
            print(f"[DEBUG] _get_user_context: Getting context for user_id={user_id}")

            # Check if user_id is valid
            if not user_id:
                print(f"[ERROR] _get_user_context: Invalid user_id={user_id}")
                return None

            # Get user's current progress
            print(f"[DEBUG] _get_user_context: Calling progress_manager.get_user_progress({user_id})")
            user_progress = self.progress_manager.get_user_progress(user_id)
            print(f"[DEBUG] _get_user_context: Progress result found: {bool(user_progress)}")

            if not user_progress:
                print(f"[WARNING] _get_user_context: No progress found for user {user_id}")
                return None

            print(f"[DEBUG] _get_user_context: Found progress - languages: {user_progress.input_language} to {user_progress.target_language}, level={user_progress.current_level}")

            # Get current topic information
            # TopicManager uses user_progress_id, not user_id
            print(f"[DEBUG] _get_user_context: Calling topic_manager.get_current_topic({user_progress.id})")
            topic_info = self.topic_manager.get_current_topic(user_progress.id)
            print(f"[DEBUG] _get_user_context: Topic info result: {topic_info}")

            if not topic_info:
                print(f"[DEBUG] _get_user_context: No current topic found, defaulting to Topic 1")
                # Default to Topic 1 if no specific topic
                topic_info = self.topic_manager.get_topic_definition(
                    user_progress.current_level, 1
                )

            # Convert topic_info to dict if it's a TopicDefinition object
            if topic_info:
                topic_dict = topic_info.to_dict() if hasattr(topic_info, 'to_dict') else topic_info
            else:
                topic_dict = None

            context = {
                'user_id': user_id,
                'input_language': user_progress.input_language,
                'target_language': user_progress.target_language,
                'level': user_progress.current_level,
                'topic_number': topic_dict.get('topic_number', 1) if topic_dict else 1,
                'topic_title': topic_dict.get('title_key', 'general') if topic_dict else 'general',
                'subtopics': topic_dict.get('subtopics', []) if topic_dict else []
            }

            print(f"[DEBUG] _get_user_context: Context built successfully")
            return context

        except Exception as e:
            print(f"[ERROR] _get_user_context: Exception occurred: {e}")
            import traceback
            print(f"[ERROR] _get_user_context: Traceback: {traceback.format_exc()}")
            return None

    def _get_topic_parameters(self, level: str, topic_number: int) -> Dict:
        """Get topic-specific parameters from database"""
        try:
            topic = self.topic_manager.get_topic_definition(level, topic_number)

            if not topic:
                return {}

            # Convert to dict if it's a TopicDefinition object
            topic_dict = topic.to_dict() if hasattr(topic, 'to_dict') else topic

            return {
                'subtopics': topic_dict.get('subtopics', []),
                'required_vocabulary': topic_dict.get('required_vocabulary', []),
                'conversation_contexts': topic_dict.get('conversation_contexts', []),
                'word_limit': topic_dict.get('word_limit'),
                'topic_specific_rules': topic_dict.get('topic_specific_rules')
            }

        except Exception as e:
            print(f"[ERROR] Getting topic parameters: {e}")
            return {}

    def _build_letter_prompt(self, context: Dict, level_rules, topic_params: Dict) -> str:
        """Build the letter generation prompt"""

        target_language = context['target_language'].capitalize()
        native_language = context['input_language'].capitalize()
        level = context['level']
        topic_title = context['topic_title']

        # Get appropriate word count for level
        if level == 'A1':
            word_count = "30-50"  # Very short for A1
            complexity = "very simple, basic"
        elif level == 'A2':
            word_count = "50-80"
            complexity = "simple, everyday"
        elif level == 'B1':
            word_count = "80-120"
            complexity = "intermediate, varied"
        else:  # B2
            word_count = "100-150"
            complexity = "advanced, natural"

        # Build topic instruction based on current topic
        topic_instruction = self._get_topic_instruction(
            context['topic_number'],
            topic_params['subtopics']
        )

        prompt = f"""You are creating an email writing exercise for a {native_language} speaker learning {target_language}.

## Student Context:
- Native Language: {native_language}
- Learning: {target_language}
- Level: {level}
- Current Topic: Topic {context['topic_number']} - {topic_title}
- Subtopics: {', '.join(topic_params.get('subtopics', []))}

## Letter Requirements:
- Language: Write ONLY in {target_language}
- Length: {word_count} words
- Complexity: {complexity} vocabulary and grammar
- Style: Informal, friendly email from a friend
- Topic Focus: {topic_instruction}

## Cultural Adaptation:
- Use culturally appropriate greeting for {target_language}
- Select an appropriate friend name for {target_language} culture
- Include cultural references natural to {target_language} speakers

## Response Prompts:
Generate 4 response prompts that:
1. Are directly related to the letter content
2. Guide the student to practice topic-specific vocabulary
3. Are appropriate for {level} level
4. Encourage varied sentence structures

## Output Format:
Generate a complete email that:
1. Starts with an appropriate greeting
2. Contains {word_count} words of content
3. Includes 2-3 questions naturally embedded
4. Ends with an appropriate closing
5. Is signed with a culturally appropriate name

After the letter, provide 4 bullet points for what the student should address in their response.

Remember: The letter must be ENTIRELY in {target_language}."""

        if level_rules and level_rules.general_guidelines:
            prompt += f"\n\n## Level {level} Guidelines:\n{level_rules.general_guidelines}"

        return prompt

    def _get_topic_instruction(self, topic_number: int, subtopics: List[str]) -> str:
        """Generate topic-specific instruction based on topic number"""

        # Map topic numbers to instruction types
        topic_instructions = {
            1: "greeting and introducing yourself",
            2: "discussing work or studies",
            3: "talking about learning and education",
            4: "discussing health or pharmacy visits",
            5: "sharing information about age and numbers",
            6: "discussing shopping and prices",
            7: "exchanging address information",
            8: "sharing personal information",
            9: "describing family members",
            10: "discussing family activities",
            11: "talking about time and weather",
            12: "making plans and appointments"
        }

        base_instruction = topic_instructions.get(topic_number, "general conversation")

        if subtopics:
            return f"{base_instruction}, focusing on {', '.join(subtopics[:2])}"

        return base_instruction

    def _get_instruction_language(self, native_language: str) -> str:
        """Map database language to Claude instruction language"""
        language_map = {
            'english': 'English',
            'german': 'German (Deutsch)',
            'spanish': 'Spanish (Español)',
            'portuguese': 'Portuguese (Português)'
        }
        return language_map.get(native_language.lower(), 'English')

    def _build_first_attempt_prompt(self, target_language: str, instruction_language: str,
                                   level: str, original_letter: str, response: str) -> str:
        """Build evaluation prompt for first attempt (hints only)"""

        return f"""You are evaluating a {target_language.capitalize()} language learner's email response.

CRITICAL: Write ALL feedback in {instruction_language.upper()}.

Student's Level: {level}
Original Letter (in {target_language.capitalize()}):
{original_letter}

Student's Response:
{response}

Analyze the response and identify errors. Group them by type and provide EDUCATIONAL HINTS only.
DO NOT give corrections or answers, only hints that guide self-discovery.

## Language-Specific Error Categories for {target_language.capitalize()}:
{self._get_error_categories(target_language)}

Return a JSON response with this structure:
{{
  "error_groups": {{
    "grammar": [
      {{"text": "<exact phrase with error>", "hint": "<educational hint only>"}}
    ],
    "vocabulary": [
      {{"text": "<phrase>", "hint": "<hint>"}}
    ],
    "spelling": [
      {{"text": "<word>", "hint": "<hint>"}}
    ],
    "{self._get_special_category(target_language)}": [
      {{"text": "<phrase>", "hint": "<hint>"}}
    ]
  }},
  "message": "<encouragement in {instruction_language}>",
  "general_feedback": "<one sentence of encouragement in {instruction_language}>"
}}

Limit to 3-4 most important errors per category."""

    def _build_second_attempt_prompt(self, target_language: str, instruction_language: str,
                                    level: str, original_letter: str,
                                    first_attempt: str, second_attempt: str) -> str:
        """Build evaluation prompt for second attempt (full feedback)"""

        return f"""You are providing comprehensive feedback on a {target_language.capitalize()} learner's email response.

CRITICAL: Write ALL feedback in {instruction_language.upper()}.

Student's Level: {level}
Original Letter (in {target_language.capitalize()}):
{original_letter}

First Attempt:
{first_attempt}

Second Attempt:
{second_attempt}

Provide detailed feedback including:
1. A corrected version that PRESERVES their message and ideas
2. Explanations for important corrections
3. Focus points for future practice
4. Overall score (0-100) based on {level} level expectations

Return a JSON response with this structure:
{{
  "original_text": "<second attempt>",
  "corrected_text": "<corrected version in {target_language.capitalize()}>",
  "explanations": [
    {{
      "error": "<what they wrote>",
      "correction": "<correct form>",
      "explanation": "<why in {instruction_language}>"
    }}
  ],
  "focus_points": [
    "<specific point to practice in {instruction_language}>",
    "<another point in {instruction_language}>"
  ],
  "score": <0-100>,
  "feedback": "<encouraging message in {instruction_language}>",
  "improvements_from_first": "<what improved in {instruction_language}>"
}}"""

    def _get_error_categories(self, target_language: str) -> str:
        """Get language-specific error categories"""

        categories = {
            'german': """- Grammar: cases, verb position, adjective endings
- Vocabulary: word choice, register, idioms
- Spelling: capitalization of nouns, umlauts
- Word Order: verb second position, sentence structure""",

            'spanish': """- Grammar: verb conjugation, gender agreement
- Vocabulary: word choice, false friends
- Spelling: accent marks, ñ usage
- Ser/Estar: correct usage of ser vs estar""",

            'portuguese': """- Grammar: verb conjugation, gender agreement
- Vocabulary: false friends with Spanish
- Spelling: accent marks, cedilla
- Contractions: preposition contractions (do, da, no, na)""",

            'english': """- Grammar: verb forms, tense usage
- Vocabulary: phrasal verbs, idioms
- Spelling: common misspellings
- Articles: a/an/the usage"""
        }

        return categories.get(target_language.lower(),
                             "- Grammar\n- Vocabulary\n- Spelling\n- Structure")

    def _get_special_category(self, target_language: str) -> str:
        """Get the special category for each language"""

        special = {
            'german': 'word_order',
            'spanish': 'ser_estar',
            'portuguese': 'contractions',
            'english': 'articles'
        }

        return special.get(target_language.lower(), 'structure')