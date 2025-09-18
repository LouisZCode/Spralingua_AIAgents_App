# Letter Templates for Spralingua Email Writing Exercise
# Handles dynamic letter generation with language-appropriate content

import random
from typing import Dict, List, Tuple

class LetterTemplates:
    """
    Generates culturally appropriate letter templates for email exercises.
    Adapts content based on target language and topic.
    """

    def __init__(self):
        """Initialize letter templates with language-specific data"""

        # Friend names by language
        self.friend_names = {
            'german': {
                'male': ['Hans', 'Klaus', 'Stefan', 'Michael', 'Thomas', 'Andreas', 'Markus', 'Daniel'],
                'female': ['Greta', 'Emma', 'Anna', 'Julia', 'Laura', 'Lisa', 'Sarah', 'Marie']
            },
            'spanish': {
                'male': ['Carlos', 'José', 'Juan', 'Miguel', 'Antonio', 'Luis', 'Pedro', 'Diego'],
                'female': ['María', 'Ana', 'Carmen', 'Isabel', 'Laura', 'Sofia', 'Elena', 'Lucia']
            },
            'portuguese': {
                'male': ['João', 'Pedro', 'António', 'Manuel', 'Paulo', 'Ricardo', 'Bruno', 'Miguel'],
                'female': ['Ana', 'Sofia', 'Maria', 'Beatriz', 'Carolina', 'Mariana', 'Rita', 'Catarina']
            },
            'english': {
                'male': ['John', 'Mike', 'David', 'James', 'Robert', 'Tom', 'William', 'Daniel'],
                'female': ['Sarah', 'Emily', 'Jessica', 'Emma', 'Lisa', 'Jennifer', 'Mary', 'Kate']
            }
        }

        # Greetings by language (informal)
        self.greetings = {
            'german': {
                'general': ['Hallo', 'Hi', 'Hey'],
                'personal': ['Lieber', 'Liebe']  # + name
            },
            'spanish': {
                'general': ['¡Hola!', '¡Hey!', '¡Qué tal!'],
                'personal': ['Querido', 'Querida']  # + name
            },
            'portuguese': {
                'general': ['Olá!', 'Oi!', 'Hey!'],
                'personal': ['Caro', 'Cara', 'Querido', 'Querida']  # + name
            },
            'english': {
                'general': ['Hi', 'Hey', 'Hello'],
                'personal': ['Dear']  # + name
            }
        }

        # Closings by language (informal)
        self.closings = {
            'german': [
                'Viele Grüße',
                'Liebe Grüße',
                'Bis bald',
                'Schöne Grüße',
                'Alles Gute'
            ],
            'spanish': [
                'Un abrazo',
                'Saludos',
                'Hasta pronto',
                'Un beso',
                'Cuídate'
            ],
            'portuguese': [
                'Um abraço',
                'Beijinhos',
                'Até breve',
                'Cumprimentos',
                'Tudo de bom'
            ],
            'english': [
                'Best wishes',
                'Take care',
                'See you soon',
                'Cheers',
                'All the best'
            ]
        }

        # How are you phrases
        self.how_are_you = {
            'german': [
                'Wie geht es dir?',
                'Wie läuft\'s?',
                'Alles gut bei dir?'
            ],
            'spanish': [
                '¿Cómo estás?',
                '¿Qué tal?',
                '¿Todo bien?'
            ],
            'portuguese': [
                'Como estás?',
                'Tudo bem?',
                'Como vais?'
            ],
            'english': [
                'How are you?',
                'How\'s it going?',
                'How have you been?'
            ]
        }

    def get_random_name(self, language: str, gender: str = None) -> str:
        """
        Get a culturally appropriate random name.

        Args:
            language: Target language
            gender: Optional gender specification ('male' or 'female')

        Returns:
            A random name appropriate for the language
        """
        names_dict = self.friend_names.get(language.lower(), self.friend_names['english'])

        if gender:
            names = names_dict.get(gender, [])
        else:
            # Mix both genders
            names = names_dict['male'] + names_dict['female']

        return random.choice(names) if names else 'Alex'

    def get_greeting(self, language: str, name: str = None, gender: str = None) -> str:
        """
        Get an appropriate greeting for the language.

        Args:
            language: Target language
            name: Optional name to include in greeting
            gender: Gender for languages that need it ('male' or 'female')

        Returns:
            Appropriate greeting string
        """
        greetings = self.greetings.get(language.lower(), self.greetings['english'])

        if name and 'personal' in greetings:
            # Use personal greeting with name
            if language.lower() == 'german':
                personal = 'Lieber' if gender == 'male' else 'Liebe'
                return f"{personal} {name}"
            elif language.lower() == 'spanish':
                personal = 'Querido' if gender == 'male' else 'Querida'
                return f"{personal} {name}"
            elif language.lower() == 'portuguese':
                if gender == 'male':
                    personal = random.choice(['Caro', 'Querido'])
                else:
                    personal = random.choice(['Cara', 'Querida'])
                return f"{personal} {name}"
            else:
                return f"Dear {name}"
        else:
            # Use general greeting
            return random.choice(greetings['general'])

    def get_closing(self, language: str) -> str:
        """
        Get an appropriate closing for the language.

        Args:
            language: Target language

        Returns:
            Appropriate closing string
        """
        closings = self.closings.get(language.lower(), self.closings['english'])
        return random.choice(closings)

    def get_how_are_you(self, language: str) -> str:
        """
        Get a 'how are you' phrase for the language.

        Args:
            language: Target language

        Returns:
            Appropriate phrase
        """
        phrases = self.how_are_you.get(language.lower(), self.how_are_you['english'])
        return random.choice(phrases)

    def parse_letter_response(self, response: str, target_language: str) -> Dict:
        """
        Parse the Claude response to extract letter and response prompts.

        Args:
            response: The full response from Claude
            target_language: The target language for the letter

        Returns:
            Dictionary with parsed letter components
        """
        import re

        # Initialize result
        result = {
            'letter': '',
            'response_prompts': [],
            'sender_name': '',
            'greeting': '',
            'closing': ''
        }

        # Simplified parsing - split by "Response Prompts:" section
        lines = response.split('\n')
        letter_lines = []
        prompts_started = False

        for line in lines:
            line = line.strip()

            # Check for response prompts section (more flexible matching)
            if any(marker in line.lower() for marker in
                   ['response prompts:', 'response:', 'respond to:', 'address:', 'in your response',
                    'en tu respuesta', 'em sua resposta', 'in ihrer antwort', 'prompts:', 
                    'responde estas preguntas', 'responde a estas preguntas']):
                prompts_started = True
                continue

            # If we're in the prompts section, extract prompts
            if prompts_started:
                # Look for bullet points or numbered items
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.')):
                    # Clean up the prompt
                    prompt = re.sub(r'^[•\-\*\d\.]\s*', '', line).strip()
                    if prompt:
                        result['response_prompts'].append(prompt)
                continue

            # If we haven't hit prompts section yet, this is letter content
            if not prompts_started:
                letter_lines.append(line)  # Include empty lines for proper spacing

        # Clean up letter content - remove empty lines at start/end
        while letter_lines and not letter_lines[0]:
            letter_lines.pop(0)
        while letter_lines and not letter_lines[-1]:
            letter_lines.pop()

        # Combine letter lines with proper line breaks
        result['letter'] = '\n'.join(letter_lines)

        # Extract sender name from the last line if it looks like a name
        if letter_lines:
            potential_name = letter_lines[-1].strip()
            if len(potential_name) < 20 and not any(char in potential_name for char in '.,!?¿¡'):
                result['sender_name'] = potential_name

        # If we didn't find prompts, create default ones
        if not result['response_prompts']:
            result['response_prompts'] = self._get_default_prompts(target_language)

        # If no sender name found, use a random one
        if not result['sender_name']:
            result['sender_name'] = self.get_random_name(target_language)

        return result

    def _is_greeting(self, line: str, language: str) -> bool:
        """Check if a line looks like a greeting"""
        greetings = self.greetings.get(language.lower(), self.greetings['english'])
        all_greetings = greetings['general'] + greetings.get('personal', [])

        return any(greeting.lower() in line.lower() for greeting in all_greetings)

    def _is_closing(self, line: str, language: str) -> bool:
        """Check if a line looks like a closing"""
        closings = self.closings.get(language.lower(), self.closings['english'])

        return any(closing.lower() in line.lower() for closing in closings)

    def _get_default_prompts(self, language: str) -> List[str]:
        """Get default response prompts if parsing fails"""

        default_prompts = {
            'german': [
                'Reagieren Sie auf die Nachricht',
                'Teilen Sie Ihre Erfahrung mit',
                'Geben Sie einen Ratschlag',
                'Stellen Sie eine Frage'
            ],
            'spanish': [
                'Responde al mensaje',
                'Comparte tu experiencia',
                'Da un consejo',
                'Haz una pregunta'
            ],
            'portuguese': [
                'Responda à mensagem',
                'Partilhe a sua experiência',
                'Dê um conselho',
                'Faça uma pergunta'
            ],
            'english': [
                'Respond to the message',
                'Share your experience',
                'Give some advice',
                'Ask a question'
            ]
        }

        return default_prompts.get(language.lower(), default_prompts['english'])

    def format_letter_for_display(self, letter_data: Dict, student_name: str = None) -> str:
        """
        Format the letter for display in the UI.

        Args:
            letter_data: Parsed letter data
            student_name: Optional student name to personalize

        Returns:
            Formatted letter HTML
        """
        if student_name:
            # Replace placeholder with actual student name if present
            letter = letter_data['letter'].replace('[Student Name]', student_name)
            letter = letter.replace('______', student_name)  # Use the already modified letter
        else:
            letter = letter_data['letter']

        # Keep natural line breaks - let CSS handle the formatting
        return letter