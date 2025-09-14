# Feedback Translator for Spralingua
# Handles translation of feedback UI elements and categories

from typing import Dict, List

class FeedbackTranslator:
    """
    Translates feedback-related UI elements and categories based on user's native language.
    Works in conjunction with FeedbackPromptBuilder for complete language adaptation.
    """

    def __init__(self):
        """Initialize the FeedbackTranslator with translation dictionaries"""
        # Category translations for each native language
        self.category_translations = {
            'english': {
                'grammar': 'Grammar',
                'vocabulary': 'Vocabulary',
                'tense': 'Tense',
                'structure': 'Structure',
                'gender': 'Gender',
                'speaking': 'Speaking',
                'ser_estar': 'Ser vs Estar',
                'contractions': 'Contractions',
                'articles': 'Articles',
                'prepositions': 'Prepositions'
            },
            'german': {
                'grammar': 'Grammatik',
                'vocabulary': 'Wortschatz',
                'tense': 'Zeitform',
                'structure': 'Satzbau',
                'gender': 'Geschlecht',
                'speaking': 'Sprechen',
                'ser_estar': 'Ser vs Estar',
                'contractions': 'Kontraktionen',
                'articles': 'Artikel',
                'prepositions': 'Präpositionen'
            },
            'spanish': {
                'grammar': 'Gramática',
                'vocabulary': 'Vocabulario',
                'tense': 'Tiempo verbal',
                'structure': 'Estructura',
                'gender': 'Género',
                'speaking': 'Conversación',
                'ser_estar': 'Ser vs Estar',
                'contractions': 'Contracciones',
                'articles': 'Artículos',
                'prepositions': 'Preposiciones'
            },
            'portuguese': {
                'grammar': 'Gramática',
                'vocabulary': 'Vocabulário',
                'tense': 'Tempo verbal',
                'structure': 'Estrutura',
                'gender': 'Gênero',
                'speaking': 'Conversação',
                'ser_estar': 'Ser vs Estar',
                'contractions': 'Contrações',
                'articles': 'Artigos',
                'prepositions': 'Preposições'
            }
        }

        # Feedback UI labels translations
        self.ui_labels = {
            'english': {
                'phrase': 'Phrase',
                'hint': 'Hint',
                'error': 'Error',
                'correction': 'Correction',
                'explanation': 'Explanation',
                'strengths': 'Strengths',
                'focus_areas': 'Areas to Focus',
                'overall_feedback': 'Overall Feedback',
                'score': 'Score',
                'top_mistakes': 'Top Mistakes',
                'praise': 'Well Done'
            },
            'german': {
                'phrase': 'Phrase',
                'hint': 'Hinweis',
                'error': 'Fehler',
                'correction': 'Korrektur',
                'explanation': 'Erklärung',
                'strengths': 'Stärken',
                'focus_areas': 'Übungsbereiche',
                'overall_feedback': 'Gesamtfeedback',
                'score': 'Punktzahl',
                'top_mistakes': 'Hauptfehler',
                'praise': 'Gut gemacht'
            },
            'spanish': {
                'phrase': 'Frase',
                'hint': 'Consejo',
                'error': 'Error',
                'correction': 'Corrección',
                'explanation': 'Explicación',
                'strengths': 'Fortalezas',
                'focus_areas': 'Áreas de Enfoque',
                'overall_feedback': 'Comentario General',
                'score': 'Puntuación',
                'top_mistakes': 'Errores Principales',
                'praise': 'Bien Hecho'
            },
            'portuguese': {
                'phrase': 'Frase',
                'hint': 'Dica',
                'error': 'Erro',
                'correction': 'Correção',
                'explanation': 'Explicação',
                'strengths': 'Pontos Fortes',
                'focus_areas': 'Áreas de Foco',
                'overall_feedback': 'Feedback Geral',
                'score': 'Pontuação',
                'top_mistakes': 'Principais Erros',
                'praise': 'Muito Bem'
            }
        }

        # Encouragement phrases by language
        self.encouragement = {
            'english': [
                "Great job!",
                "Keep up the good work!",
                "You're making excellent progress!",
                "Well done!",
                "Fantastic effort!"
            ],
            'german': [
                "Gut gemacht!",
                "Weiter so!",
                "Du machst ausgezeichnete Fortschritte!",
                "Sehr gut!",
                "Fantastische Leistung!"
            ],
            'spanish': [
                "¡Buen trabajo!",
                "¡Sigue así!",
                "¡Estás progresando excelentemente!",
                "¡Muy bien!",
                "¡Esfuerzo fantástico!"
            ],
            'portuguese': [
                "Bom trabalho!",
                "Continue assim!",
                "Está a fazer excelentes progressos!",
                "Muito bem!",
                "Esforço fantástico!"
            ]
        }

    def get_categories_translated(self, native_language: str, categories: List[str]) -> Dict[str, str]:
        """
        Get translated category names for the given native language.

        Args:
            native_language: The user's native language
            categories: List of category keys to translate

        Returns:
            Dictionary mapping category keys to translated names
        """
        language_lower = native_language.lower()
        if language_lower not in self.category_translations:
            language_lower = 'english'  # Fallback to English

        translations = self.category_translations[language_lower]
        result = {}
        for category in categories:
            result[category] = translations.get(category, category.capitalize())

        return result

    def get_ui_label(self, native_language: str, label_key: str) -> str:
        """
        Get a translated UI label.

        Args:
            native_language: The user's native language
            label_key: The key of the label to translate

        Returns:
            Translated label text
        """
        language_lower = native_language.lower()
        if language_lower not in self.ui_labels:
            language_lower = 'english'  # Fallback to English

        labels = self.ui_labels[language_lower]
        return labels.get(label_key, label_key.replace('_', ' ').capitalize())

    def get_all_ui_labels(self, native_language: str) -> Dict[str, str]:
        """
        Get all UI labels translated for the given native language.

        Args:
            native_language: The user's native language

        Returns:
            Dictionary of all translated UI labels
        """
        language_lower = native_language.lower()
        if language_lower not in self.ui_labels:
            language_lower = 'english'  # Fallback to English

        return self.ui_labels[language_lower].copy()

    def get_encouragement_phrase(self, native_language: str, index: int = 0) -> str:
        """
        Get an encouragement phrase in the user's native language.

        Args:
            native_language: The user's native language
            index: Index of the phrase to get (0-4)

        Returns:
            Encouragement phrase in the native language
        """
        language_lower = native_language.lower()
        if language_lower not in self.encouragement:
            language_lower = 'english'  # Fallback to English

        phrases = self.encouragement[language_lower]
        # Ensure index is within bounds
        index = min(index, len(phrases) - 1)
        return phrases[index]

    def get_category_descriptions(self, target_language: str, native_language: str) -> Dict[str, str]:
        """
        Get category descriptions translated for the native language,
        specific to the target language being learned.

        Args:
            target_language: The language being learned
            native_language: The user's native language

        Returns:
            Dictionary of category descriptions in native language
        """
        # This would contain more detailed descriptions for each category
        # For now, returning basic translations
        categories = self._get_target_language_categories(target_language)
        return self.get_categories_translated(native_language, categories)

    def _get_target_language_categories(self, target_language: str) -> List[str]:
        """
        Get the list of relevant categories for a target language.

        Args:
            target_language: The language being learned

        Returns:
            List of category keys relevant to that language
        """
        common_categories = ['grammar', 'vocabulary', 'tense', 'structure', 'speaking']

        language_specific = {
            'german': ['gender', 'articles'],
            'spanish': ['ser_estar', 'gender'],
            'portuguese': ['contractions', 'gender'],
            'english': ['articles', 'prepositions']
        }

        categories = common_categories.copy()
        if target_language.lower() in language_specific:
            categories.extend(language_specific[target_language.lower()])

        return categories