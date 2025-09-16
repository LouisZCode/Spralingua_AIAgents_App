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

CRITICAL: Write ALL feedback in {response_language.upper()}.
The "hint" field must be in {response_language}, NOT in {target_language.capitalize()}.

CRITICAL PHRASE RULE:
- The "phrase" field MUST contain the EXACT text from the student's message
- NEVER translate the phrase to another language
- When referring to {target_language.capitalize()} words in your hint, keep them in {target_language.capitalize()} and put them in quotes
- Example: For Spanish speaker learning English who wrote "hello", your hint in Spanish should say "Usa 'hello' para..." NOT "Usa 'hola' para..."

Student message: {{message}}
Language level: {{level}}

IMPORTANT CORRECTNESS RULE:
- If the {target_language.capitalize()} is correct and natural, give PRAISE (type: "praise")
- Do NOT invent errors where none exist
- For {{level}} level: Basic statements and common phrases should be recognized as correct
- Examples of ALWAYS CORRECT {target_language.capitalize()} phrases that deserve praise:
  * Basic introductions: "I am from [country]", "My name is [name]"
  * Common greetings: "Hello", "How are you?", "Thank you", "Goodbye"
  * Simple correct statements at any level

SPEECH RECOGNITION RULE:
- IGNORE missing punctuation marks (? ! . , : ;) - speech recognition cannot capture these
- "Where are you from" and "Where are you from?" are BOTH CORRECT when spoken
- "How are you" and "How are you?" are BOTH CORRECT when spoken
- Focus ONLY on word choice, grammar, verb forms, and sentence structure
- Do NOT mark as error: missing question marks, periods, exclamation points, or commas
- Only flag punctuation if the WORDS themselves indicate wrong sentence type

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
- The "phrase" MUST be verbatim from the message (never translated)
- The "hint" is maximum 15 words, written in {response_language}
- Recognize correct usage: If it's right, praise it (don't invent errors)
- For errors: Give guidance, but DON'T reveal the complete solution
- For warnings: Suggest improvements for already acceptable usage
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

SPEECH RECOGNITION NOTE:
- These messages were spoken, not typed - ignore missing punctuation (? ! . , : ;)
- Focus on word choice, grammar, and structure errors only
- "Where are you from" without "?" is NOT an error in speech

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
ERROR Examples:
Message: "Mit meine Freunde war es toll"
{"phrase": "meine Freunde", "hint": "Nach 'mit' verwende Dativ: 'meinen Freunden'", "category": "grammar", "type": "error"}

Message: "Ich bin kalt"
{"phrase": "bin kalt", "hint": "Für Gefühle nutze 'mir ist': 'mir ist kalt'", "category": "vocabulary", "type": "error"}

Message: "Ich habe es gemacht für dich"
{"phrase": "gemacht für dich", "hint": "Wortstellung: 'für dich gemacht'", "category": "structure", "type": "error"}

WARNING Examples:
Message: "Seit drei Jahren lerne ich Deutsch"
{"phrase": "Seit drei Jahren lerne", "hint": "Korrekt, aber üblicher: Verb an Position 2", "category": "structure", "type": "warning"}

Message: "Ich will nach Berlin fahren"
{"phrase": "will", "hint": "'Will' ist ok, 'möchte' klingt höflicher", "category": "speaking", "type": "warning"}

Message: "Das Haus von meinem Vater"
{"phrase": "von meinem Vater", "hint": "Genitiv 'meines Vaters' ist eleganter", "category": "grammar", "type": "warning"}

PRAISE Examples:
Message: "Ich komme aus Spanien"
{"phrase": "komme aus", "hint": "Perfekt! Richtige Form für Herkunft", "category": "structure", "type": "praise"}

Message: "Ich habe gestern eingekauft"
{"phrase": "habe eingekauft", "hint": "Super! Perfekt mit trennbarem Verb", "category": "grammar", "type": "praise"}

Message: "Könnten Sie mir bitte helfen?"
{"phrase": "Könnten Sie", "hint": "Ausgezeichnet! Sehr höfliche Form", "category": "speaking", "type": "praise"}""",

            'spanish': """
ERROR Examples:
Message: "Yo soy muy cansado hoy"
{"phrase": "soy cansado", "hint": "Para estados temporales usa 'estoy cansado'", "category": "ser_estar", "type": "error"}

Message: "He vivido aquí para cinco años"
{"phrase": "para cinco años", "hint": "Para duración usa 'por': 'por cinco años'", "category": "prepositions", "type": "error"}

Message: "Pienso de que es bueno"
{"phrase": "pienso de que", "hint": "Después de 'pensar' no uses 'de': 'pienso que'", "category": "grammar", "type": "error"}

WARNING Examples:
Message: "Yo quiero comer ahora"
{"phrase": "Yo quiero", "hint": "Correcto, pero 'yo' es opcional aquí", "category": "structure", "type": "warning"}

Message: "La gente están contentas"
{"phrase": "están contentas", "hint": "'La gente' es singular: 'está contenta'", "category": "grammar", "type": "warning"}

Message: "Voy a ir mañana"
{"phrase": "Voy a ir", "hint": "Correcto pero redundante, mejor solo 'voy'", "category": "vocabulary", "type": "warning"}

PRAISE Examples:
Message: "Soy de México"
{"phrase": "Soy de", "hint": "¡Perfecto! Forma correcta para origen", "category": "structure", "type": "praise"}

Message: "He estado trabajando toda la mañana"
{"phrase": "He estado trabajando", "hint": "¡Excelente! Perfecto continuo bien usado", "category": "tense", "type": "praise"}

Message: "¿Me podría ayudar, por favor?"
{"phrase": "Me podría", "hint": "¡Muy bien! Forma muy cortés", "category": "speaking", "type": "praise"}""",

            'portuguese': """
ERROR Examples:
Message: "Eu gosto de a música"
{"phrase": "de a música", "hint": "Use a contração 'da' em vez de 'de a'", "category": "contractions", "type": "error"}

Message: "Eu sou cansado hoje"
{"phrase": "sou cansado", "hint": "Para estados temporários: 'estou cansado'", "category": "ser_estar", "type": "error"}

Message: "Fazem cinco anos que moro aqui"
{"phrase": "Fazem cinco anos", "hint": "Com tempo use 'Faz' (singular)", "category": "grammar", "type": "error"}

WARNING Examples:
Message: "Estou vivendo aqui há cinco anos"
{"phrase": "Estou vivendo", "hint": "Correto, mas 'vivo' é mais natural", "category": "tense", "type": "warning"}

Message: "Eu próprio fiz isso"
{"phrase": "Eu próprio", "hint": "Ok, mas 'Eu mesmo' é mais comum", "category": "vocabulary", "type": "warning"}

Message: "Vou no mercado"
{"phrase": "Vou no", "hint": "Melhor usar 'vou ao mercado'", "category": "prepositions", "type": "warning"}

PRAISE Examples:
Message: "Sou do Brasil"
{"phrase": "Sou do", "hint": "Perfeito! Contração correta 'de + o'", "category": "contractions", "type": "praise"}

Message: "Tenho estudado português há meses"
{"phrase": "Tenho estudado", "hint": "Excelente! Pretérito perfeito composto", "category": "tense", "type": "praise"}

Message: "Poderia me ajudar, por favor?"
{"phrase": "Poderia me", "hint": "Muito bem! Forma educada perfeita", "category": "speaking", "type": "praise"}""",

            'english': """
ERROR Examples:
Message: "I have been to London last year"
{"phrase": "have been", "hint": "Con 'last year' usa pasado simple: 'went'", "category": "tense", "type": "error"}

Message: "She suggested me to go"
{"phrase": "suggested me to", "hint": "Después de 'suggest' usa 'that I go' o 'going'", "category": "grammar", "type": "error"}

Message: "I am boring in this class"
{"phrase": "am boring", "hint": "Usa 'am bored' cuando tú sientes aburrimiento", "category": "vocabulary", "type": "error"}

WARNING Examples:
Message: "I will call you when I will arrive"
{"phrase": "when I will", "hint": "Después de 'when' usa presente: 'when I arrive'", "category": "grammar", "type": "warning"}

Message: "Can you borrow me your pen?"
{"phrase": "borrow me", "hint": "Considera 'lend me' o 'Can I borrow'", "category": "vocabulary", "type": "warning"}

Message: "I'm living here since 2020"
{"phrase": "I'm living", "hint": "Con 'since' mejor usa 'have lived'", "category": "tense", "type": "warning"}

PRAISE Examples:
Message: "I am from Mexico"
{"phrase": "I am from", "hint": "¡Perfecto! Forma correcta para decir tu origen", "category": "structure", "type": "praise"}

Message: "I've been working here for five years"
{"phrase": "have been working", "hint": "¡Excelente! Uso correcto del present perfect continuous", "category": "tense", "type": "praise"}

Message: "Could you please help me?"
{"phrase": "Could you please", "hint": "¡Muy bien! Forma educada de pedir ayuda", "category": "speaking", "type": "praise"}"""
        }

        # Default example if language not found
        default_example = """
Message: "The sentence with an error"
{"phrase": "with an error", "hint": "Check this construction", "category": "grammar", "type": "error"}"""

        return examples.get(target_language.lower(), default_example)