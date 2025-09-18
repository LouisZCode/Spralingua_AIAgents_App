# Email Feedback Builder for Spralingua
# Handles feedback generation and translation for email exercises

from typing import Dict, List

class EmailFeedbackBuilder:
    """
    Builds and translates feedback for email writing exercises.
    Extends the pattern from FeedbackPromptBuilder for email-specific needs.
    """

    def __init__(self):
        """Initialize the EmailFeedbackBuilder with translation dictionaries"""
        # UI translations for feedback elements
        self.ui_translations = {
            'english': {
                'feedback_title': 'Feedback',
                'first_attempt_title': 'Areas for Improvement',
                'second_attempt_title': 'Comprehensive Feedback',
                'errors_found': 'Errors Found',
                'grammar_errors': 'Grammar',
                'vocabulary_errors': 'Vocabulary',
                'spelling_errors': 'Spelling',
                'your_response': 'Your Response',
                'corrected_version': 'Corrected Version',
                'explanations': 'Explanations',
                'focus_areas': 'Focus Areas',
                'score': 'Score',
                'improvements': 'Improvements from First Attempt',
                'well_done': 'Well Done!',
                'keep_trying': 'Keep Trying!',
                'good_effort': 'Good Effort!',
                'excellent': 'Excellent!',
                'needs_work': 'Needs More Practice'
            },
            'german': {
                'feedback_title': 'Rückmeldung',
                'first_attempt_title': 'Verbesserungsbereiche',
                'second_attempt_title': 'Ausführliche Rückmeldung',
                'errors_found': 'Gefundene Fehler',
                'grammar_errors': 'Grammatik',
                'vocabulary_errors': 'Wortschatz',
                'spelling_errors': 'Rechtschreibung',
                'your_response': 'Ihre Antwort',
                'corrected_version': 'Korrigierte Version',
                'explanations': 'Erklärungen',
                'focus_areas': 'Schwerpunkte',
                'score': 'Punktzahl',
                'improvements': 'Verbesserungen vom ersten Versuch',
                'well_done': 'Gut gemacht!',
                'keep_trying': 'Weiter versuchen!',
                'good_effort': 'Gute Bemühung!',
                'excellent': 'Ausgezeichnet!',
                'needs_work': 'Benötigt mehr Übung'
            },
            'spanish': {
                'feedback_title': 'Retroalimentación',
                'first_attempt_title': 'Áreas de Mejora',
                'second_attempt_title': 'Retroalimentación Completa',
                'errors_found': 'Errores Encontrados',
                'grammar_errors': 'Gramática',
                'vocabulary_errors': 'Vocabulario',
                'spelling_errors': 'Ortografía',
                'your_response': 'Tu Respuesta',
                'corrected_version': 'Versión Corregida',
                'explanations': 'Explicaciones',
                'focus_areas': 'Áreas de Enfoque',
                'score': 'Puntuación',
                'improvements': 'Mejoras desde el Primer Intento',
                'well_done': '¡Bien hecho!',
                'keep_trying': '¡Sigue intentando!',
                'good_effort': '¡Buen esfuerzo!',
                'excellent': '¡Excelente!',
                'needs_work': 'Necesita más práctica'
            },
            'portuguese': {
                'feedback_title': 'Feedback',
                'first_attempt_title': 'Áreas de Melhoria',
                'second_attempt_title': 'Feedback Completo',
                'errors_found': 'Erros Encontrados',
                'grammar_errors': 'Gramática',
                'vocabulary_errors': 'Vocabulário',
                'spelling_errors': 'Ortografia',
                'your_response': 'Sua Resposta',
                'corrected_version': 'Versão Corrigida',
                'explanations': 'Explicações',
                'focus_areas': 'Áreas de Foco',
                'score': 'Pontuação',
                'improvements': 'Melhorias desde a Primeira Tentativa',
                'well_done': 'Muito bem!',
                'keep_trying': 'Continue tentando!',
                'good_effort': 'Bom esforço!',
                'excellent': 'Excelente!',
                'needs_work': 'Precisa de mais prática'
            }
        }

        # Response prompt translations
        self.prompt_translations = {
            'english': {
                'greeting': 'Greet the person',
                'introduction': 'Introduce yourself',
                'ask_origin': 'Ask where they are from',
                'share_experience': 'Share your experience',
                'give_opinion': 'Give your opinion',
                'make_suggestion': 'Make a suggestion',
                'ask_question': 'Ask a question',
                'express_interest': 'Express interest',
                'make_plans': 'Make future plans',
                'say_goodbye': 'Say goodbye politely'
            },
            'german': {
                'greeting': 'Begrüßen Sie die Person',
                'introduction': 'Stellen Sie sich vor',
                'ask_origin': 'Fragen Sie, woher sie kommen',
                'share_experience': 'Teilen Sie Ihre Erfahrung',
                'give_opinion': 'Geben Sie Ihre Meinung ab',
                'make_suggestion': 'Machen Sie einen Vorschlag',
                'ask_question': 'Stellen Sie eine Frage',
                'express_interest': 'Zeigen Sie Interesse',
                'make_plans': 'Machen Sie Zukunftspläne',
                'say_goodbye': 'Verabschieden Sie sich höflich'
            },
            'spanish': {
                'greeting': 'Saluda a la persona',
                'introduction': 'Preséntate',
                'ask_origin': 'Pregunta de dónde es',
                'share_experience': 'Comparte tu experiencia',
                'give_opinion': 'Da tu opinión',
                'make_suggestion': 'Haz una sugerencia',
                'ask_question': 'Haz una pregunta',
                'express_interest': 'Expresa interés',
                'make_plans': 'Haz planes futuros',
                'say_goodbye': 'Despídete cortésmente'
            },
            'portuguese': {
                'greeting': 'Cumprimente a pessoa',
                'introduction': 'Apresente-se',
                'ask_origin': 'Pergunte de onde ela é',
                'share_experience': 'Compartilhe sua experiência',
                'give_opinion': 'Dê sua opinião',
                'make_suggestion': 'Faça uma sugestão',
                'ask_question': 'Faça uma pergunta',
                'express_interest': 'Expresse interesse',
                'make_plans': 'Faça planos futuros',
                'say_goodbye': 'Despeça-se educadamente'
            }
        }

    def get_ui_translations(self, native_language: str) -> Dict[str, str]:
        """
        Get UI translations for the user's native language.

        Args:
            native_language: The user's native language

        Returns:
            Dictionary of translated UI elements
        """
        return self.ui_translations.get(
            native_language.lower(),
            self.ui_translations['english']
        )

    def get_response_prompts(self, topic_number: int, native_language: str) -> List[str]:
        """
        Get response prompts based on topic and native language.

        Args:
            topic_number: The current topic number (1-12)
            native_language: The user's native language

        Returns:
            List of 4 translated response prompts
        """
        prompts = self.prompt_translations.get(
            native_language.lower(),
            self.prompt_translations['english']
        )

        # Map topic numbers to appropriate prompts
        topic_prompt_map = {
            1: ['greeting', 'introduction', 'ask_origin', 'say_goodbye'],
            2: ['greeting', 'share_experience', 'ask_question', 'express_interest'],
            3: ['greeting', 'give_opinion', 'share_experience', 'ask_question'],
            4: ['greeting', 'share_experience', 'make_suggestion', 'express_interest'],
            5: ['greeting', 'share_experience', 'ask_question', 'give_opinion'],
            6: ['greeting', 'give_opinion', 'make_suggestion', 'ask_question'],
            7: ['greeting', 'share_experience', 'ask_question', 'make_plans'],
            8: ['greeting', 'share_experience', 'express_interest', 'ask_question'],
            9: ['greeting', 'share_experience', 'give_opinion', 'express_interest'],
            10: ['greeting', 'share_experience', 'make_plans', 'ask_question'],
            11: ['greeting', 'give_opinion', 'make_suggestion', 'make_plans'],
            12: ['greeting', 'make_plans', 'express_interest', 'say_goodbye']
        }

        prompt_keys = topic_prompt_map.get(topic_number,
                                          ['greeting', 'share_experience', 'ask_question', 'say_goodbye'])

        return [prompts[key] for key in prompt_keys]

    def format_feedback_html(self, feedback_data: Dict, attempt: int,
                            native_language: str) -> str:
        """
        Format feedback data into HTML for display.

        Args:
            feedback_data: The feedback data from evaluation
            attempt: 1 or 2 (first or second attempt)
            native_language: User's native language for UI

        Returns:
            HTML string for feedback display
        """
        ui_text = self.get_ui_translations(native_language)

        if attempt == 1:
            return self._format_first_attempt_feedback(feedback_data, ui_text)
        else:
            return self._format_second_attempt_feedback(feedback_data, ui_text)

    def _format_first_attempt_feedback(self, data: Dict, ui_text: Dict) -> str:
        """Format first attempt feedback (hints only)"""

        html_parts = [f'<h3>{ui_text["first_attempt_title"]}</h3>']

        if data.get('message'):
            html_parts.append(f'<p class="feedback-message">{data["message"]}</p>')

        error_groups = data.get('error_groups', {})

        for category, errors in error_groups.items():
            if errors:
                category_label = ui_text.get(f'{category}_errors', category.capitalize())
                html_parts.append(f'<div class="error-category">')
                html_parts.append(f'<h4>{category_label}</h4>')
                html_parts.append('<ul>')

                for error in errors[:4]:  # Limit to 4 errors per category
                    html_parts.append('<li>')
                    html_parts.append(f'<span class="error-text">"{error.get("text", "")}"</span>')
                    html_parts.append(f'<span class="error-hint">{error.get("hint", "")}</span>')
                    html_parts.append('</li>')

                html_parts.append('</ul>')
                html_parts.append('</div>')

        if data.get('general_feedback'):
            html_parts.append(f'<p class="general-feedback">{data["general_feedback"]}</p>')

        return '\n'.join(html_parts)

    def _format_second_attempt_feedback(self, data: Dict, ui_text: Dict) -> str:
        """Format second attempt feedback (full corrections)"""

        html_parts = [f'<h3>{ui_text["second_attempt_title"]}</h3>']

        # Score
        score = data.get('score', 0)
        score_class = self._get_score_class(score)
        score_label = self._get_score_label(score, ui_text)

        html_parts.append(f'<div class="score-section {score_class}">')
        html_parts.append(f'<span class="score-label">{ui_text["score"]}:</span>')
        html_parts.append(f'<span class="score-value">{score}/100</span>')
        html_parts.append(f'<span class="score-message">{score_label}</span>')
        html_parts.append('</div>')

        # Overall feedback
        if data.get('feedback'):
            html_parts.append(f'<p class="overall-feedback">{data["feedback"]}</p>')

        # Improvements from first attempt
        if data.get('improvements_from_first'):
            html_parts.append(f'<div class="improvements">')
            html_parts.append(f'<h4>{ui_text["improvements"]}</h4>')
            html_parts.append(f'<p>{data["improvements_from_first"]}</p>')
            html_parts.append('</div>')

        # Corrected version
        if data.get('corrected_text'):
            html_parts.append('<div class="correction-section">')
            html_parts.append(f'<h4>{ui_text["corrected_version"]}</h4>')
            html_parts.append(f'<div class="corrected-text">{data["corrected_text"]}</div>')
            html_parts.append('</div>')

        # Explanations
        if data.get('explanations'):
            html_parts.append('<div class="explanations-section">')
            html_parts.append(f'<h4>{ui_text["explanations"]}</h4>')
            html_parts.append('<ul>')

            for exp in data['explanations'][:5]:  # Limit to 5 explanations
                html_parts.append('<li>')
                html_parts.append(f'<span class="error-original">"{exp.get("error", "")}"</span>')
                html_parts.append(' → ')
                html_parts.append(f'<span class="error-correction">"{exp.get("correction", "")}"</span>')
                html_parts.append(f'<p class="error-explanation">{exp.get("explanation", "")}</p>')
                html_parts.append('</li>')

            html_parts.append('</ul>')
            html_parts.append('</div>')

        # Focus points
        if data.get('focus_points'):
            html_parts.append('<div class="focus-points">')
            html_parts.append(f'<h4>{ui_text["focus_areas"]}</h4>')
            html_parts.append('<ul>')

            for point in data['focus_points']:
                html_parts.append(f'<li>{point}</li>')

            html_parts.append('</ul>')
            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _get_score_class(self, score: int) -> str:
        """Get CSS class based on score"""
        if score >= 85:
            return 'score-excellent'
        elif score >= 70:
            return 'score-good'
        elif score >= 50:
            return 'score-fair'
        else:
            return 'score-needs-work'

    def _get_score_label(self, score: int, ui_text: Dict) -> str:
        """Get score label based on score value"""
        if score >= 85:
            return ui_text['excellent']
        elif score >= 70:
            return ui_text['well_done']
        elif score >= 50:
            return ui_text['good_effort']
        else:
            return ui_text['needs_work']