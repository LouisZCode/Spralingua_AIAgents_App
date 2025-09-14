# Feedback Prompt Builder for Spralingua
# Dynamic feedback prompt generation based on language pair

from typing import Dict, List

class FeedbackPromptBuilder:
    """
    Generates dynamic feedback prompts based on target and native languages.
    Separated from character personalities for clean architecture.
    """

    def __init__(self):
        """Initialize the FeedbackPromptBuilder with language configurations"""
        pass

    def _get_prompt_language(self, native_language: str) -> str:
        """
        Map database language to Claude instruction language.

        Args:
            native_language: The user's native language from database

        Returns:
            Language instruction for Claude (e.g., 'German (Deutsch)')
        """
        language_map = {
            'english': 'English',
            'german': 'German (Deutsch)',
            'spanish': 'Spanish (Español)',
            'portuguese': 'Portuguese (Português)'
        }
        return language_map.get(native_language.lower(), 'English')

    def get_hint_prompt(self, target_language: str, native_language: str, level: str) -> str:
        """
        Generate a language hint prompt for analyzing a single message.

        Args:
            target_language: The language being learned (e.g., 'german', 'spanish')
            native_language: The user's native language (e.g., 'english', 'portuguese')
            level: The user's proficiency level (e.g., 'beginner', 'intermediate')

        Returns:
            A prompt string for generating language hints
        """
        # Get the language for Claude to respond in
        response_language = self._get_prompt_language(native_language)

        categories = self.get_language_categories(target_language)
        categories_text = '\n'.join([f'  - "{cat["key"]}" - {cat["description"]}' for cat in categories])

        prompt = f"""You are a helpful {target_language.capitalize()} language coach. Analyze the following message from a {target_language.capitalize()} learner and provide ONE specific, categorized hint.

CRITICAL: The "hint" field MUST be written in {response_language.upper()}.
Do NOT write the hint in English unless {response_language} is English.

Student message: {{message}}
Language level: {{level}}

ANALYZE the message and choose ONE specific phrase that either:
- Was used particularly well (for praise)
- Could be improved (for helpful feedback)

Respond ONLY with a JSON object in this format:
{{
  "phrase": "<exact phrase from the message>",
  "hint": "<specific hint about this phrase - MUST BE IN {response_language.upper()}>",
  "category": "<category>",
  "type": "<error|warning|praise>"
}}

CATEGORIES:
{categories_text}

EXAMPLES for {target_language.capitalize()}:
{self._get_hint_examples(target_language)}

RULES:
- The "phrase" MUST be verbatim from the message
- The "hint" is maximum 15 words, in {response_language}
- For errors: Give guidance, but DON'T reveal the solution
- Always be encouraging and constructive
- Return ONLY the JSON object, nothing else"""

        return prompt

    def get_comprehensive_feedback_prompt(self, target_language: str, native_language: str, level: str) -> str:
        """
        Generate a comprehensive feedback prompt for analyzing multiple messages.

        Args:
            target_language: The language being learned
            native_language: The user's native language
            level: The user's proficiency level

        Returns:
            A prompt string for generating comprehensive feedback
        """
        # Get the language for Claude to respond in
        response_language = self._get_prompt_language(native_language)

        prompt = f"""You are an experienced {target_language.capitalize()} language coach. Analyze the following messages from a {target_language.capitalize()} learner and create detailed feedback in JSON format.

CRITICAL LANGUAGE REQUIREMENT:
All text in "explanation", "praise", "focus_areas", and "overall_feedback" fields MUST be in {response_language.upper()}.
Do NOT use English unless {response_language} is English.
Only the "error" phrases should remain as originally written by the student.

Student messages:
{{messages}}

Language level: {{level}}

IMPORTANT: This is AFTER the practice session - now provide COMPLETE CORRECTIONS with explanations (not just hints).

Create a JSON response with this format:
{{
  "top_mistakes": [
    {{
      "error": "<exact phrase from the messages>",
      "correction": "<correct version>",
      "explanation": "<explanation in {response_language} of why the correction is right>"
    }}
  ],
  "strengths": [
    {{
      "phrase": "<well-used phrase>",
      "praise": "<specific praise for this usage in {response_language}>"
    }}
  ],
  "focus_areas": [
    "Specific grammar point based on the errors (in {response_language})",
    "Another area for practice (in {response_language})"
  ],
  "overall_feedback": "Encouraging overall feedback about progress (in {response_language})",
  "score": <score 0-100 based on level and performance>
}}

RULES:
1. Choose the 3-5 MOST IMPORTANT errors from all messages
2. Be specific with corrections and explanations
3. Highlight at least 2 strengths
4. Suggest 2-3 focus areas for improvement
5. Keep explanations clear and helpful
6. Base the score on the {level} level expectations
7. ALL feedback text should be in {response_language} (except the error phrases which remain as written)

Remember: This is educational feedback after practice, so be thorough but encouraging."""

        return prompt

    def get_language_categories(self, target_language: str) -> List[Dict[str, str]]:
        """
        Get language-specific error categories for feedback.

        Args:
            target_language: The target language

        Returns:
            List of category dictionaries with key and description
        """
        categories = {
            'german': [
                {'key': 'grammar', 'description': 'verb conjugation, cases, adjective endings'},
                {'key': 'vocabulary', 'description': 'word choice, false friends, prepositions'},
                {'key': 'tense', 'description': 'verb tense usage, auxiliary verbs, past participle'},
                {'key': 'structure', 'description': 'word order, sentence construction'},
                {'key': 'gender', 'description': 'article errors, gender agreement'},
                {'key': 'speaking', 'description': 'common spoken German patterns'}
            ],
            'spanish': [
                {'key': 'grammar', 'description': 'verb conjugation, subjunctive mood, reflexive verbs'},
                {'key': 'vocabulary', 'description': 'word choice, false friends, prepositions'},
                {'key': 'tense', 'description': 'preterite vs imperfect, compound tenses'},
                {'key': 'structure', 'description': 'word order, sentence construction'},
                {'key': 'gender', 'description': 'article and adjective agreement'},
                {'key': 'ser_estar', 'description': 'ser vs estar usage'},
                {'key': 'speaking', 'description': 'common spoken Spanish patterns'}
            ],
            'portuguese': [
                {'key': 'grammar', 'description': 'verb conjugation, personal infinitive, subjunctive'},
                {'key': 'vocabulary', 'description': 'word choice, false friends with Spanish'},
                {'key': 'tense', 'description': 'verb tenses, continuous forms'},
                {'key': 'structure', 'description': 'word order, sentence construction'},
                {'key': 'gender', 'description': 'article and adjective agreement'},
                {'key': 'contractions', 'description': 'preposition contractions (do, da, no, na)'},
                {'key': 'speaking', 'description': 'common spoken Portuguese patterns'}
            ],
            'english': [
                {'key': 'grammar', 'description': 'verb forms, conditionals, modal verbs'},
                {'key': 'vocabulary', 'description': 'word choice, phrasal verbs, idioms'},
                {'key': 'tense', 'description': 'present perfect vs past simple, continuous forms'},
                {'key': 'structure', 'description': 'word order, question formation'},
                {'key': 'articles', 'description': 'a/an/the usage, zero article'},
                {'key': 'prepositions', 'description': 'in/on/at, phrasal verb particles'},
                {'key': 'speaking', 'description': 'common spoken English patterns'}
            ]
        }

        # Default to general categories if language not found
        default_categories = [
            {'key': 'grammar', 'description': 'verb forms, sentence structure'},
            {'key': 'vocabulary', 'description': 'word choice, appropriate usage'},
            {'key': 'structure', 'description': 'word order, sentence construction'},
            {'key': 'speaking', 'description': 'natural language patterns'}
        ]

        return categories.get(target_language.lower(), default_categories)

    def _get_hint_examples(self, target_language: str) -> str:
        """
        Get language-specific examples for hint generation.

        Args:
            target_language: The target language

        Returns:
            Example hints for the specific language
        """
        examples = {
            'german': """
Message: "Ich bin gestern ins Kino gegangen"
{"phrase": "bin gegangen", "hint": "<PRAISE IN YOUR RESPONSE LANGUAGE>", "category": "tense", "type": "praise"}

Message: "Ich habe nach Hause gefahren"
{"phrase": "habe gefahren", "hint": "<ERROR HINT IN YOUR RESPONSE LANGUAGE>", "category": "tense", "type": "error"}

Message: "Mit meine Freunde war es toll"
{"phrase": "mit meine Freunde", "hint": "<GRAMMAR HINT IN YOUR RESPONSE LANGUAGE>", "category": "grammar", "type": "error"}""",

            'spanish': """
Message: "Ayer fui al cine con mis amigos"
{"phrase": "fui al cine", "hint": "Great use of preterite for completed action!", "category": "tense", "type": "praise"}

Message: "Yo soy muy cansado hoy"
{"phrase": "soy cansado", "hint": "Temporary states like 'tired' use a different verb", "category": "ser_estar", "type": "error"}

Message: "He vivido aquí para cinco años"
{"phrase": "para cinco años", "hint": "Duration of time uses a different preposition", "category": "vocabulary", "type": "error"}""",

            'portuguese': """
Message: "Eu fui ao cinema ontem"
{"phrase": "fui ao cinema", "hint": "Perfect use of 'ao' contraction!", "category": "contractions", "type": "praise"}

Message: "Estou vivendo aqui há cinco anos"
{"phrase": "estou vivendo", "hint": "Great use of continuous form!", "category": "tense", "type": "praise"}

Message: "Eu gosto de a música"
{"phrase": "de a música", "hint": "This preposition needs contraction with the article", "category": "contractions", "type": "error"}""",

            'english': """
Message: "I have been to London last year"
{"phrase": "have been", "hint": "Specific past time requires different tense", "category": "tense", "type": "error"}

Message: "She suggested me to go"
{"phrase": "suggested me to", "hint": "Check the pattern after 'suggest'", "category": "grammar", "type": "error"}

Message: "I've been working here for five years"
{"phrase": "have been working", "hint": "Excellent use of present perfect continuous!", "category": "tense", "type": "praise"}"""
        }

        # Default example if language not found
        default_example = """
Message: "The sentence with an error"
{"phrase": "with an error", "hint": "Check this construction", "category": "grammar", "type": "error"}"""

        return examples.get(target_language.lower(), default_example)