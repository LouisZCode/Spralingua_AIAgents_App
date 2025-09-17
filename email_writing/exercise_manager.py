"""Email Exercise manager for Spralingua."""

import json
import re
import random
from typing import Dict, Any, Optional, Tuple
from prompt_manager import PromptManager
from claude_client import ClaudeClient
from models.user import User


class EmailExerciseManager:
    """Manages email writing exercise logic and AI interactions."""

    def __init__(self, exercise_prompts_path: str):
        """
        Initialize the exercise manager.

        Args:
            exercise_prompts_path: Path to the exercise-specific prompts YAML file
        """
        self.prompt_manager = PromptManager(exercise_prompts_path)
        self.claude_client = None  # Will be initialized per request

    def process_exercise_request(self, action: str, data: dict, user_context: dict,
                                session_data: dict = None) -> Tuple[bool, dict]:
        """
        Process an exercise request and return JSON response.

        Args:
            action: The action to perform (e.g., 'generate', 'evaluate')
            data: Request data from the frontend
            user_context: User information (user_id, session_id, etc.)
            session_data: Session data for storing state between requests

        Returns:
            Tuple of (success, response_data)
        """
        try:
            # Initialize Claude client
            self.claude_client = ClaudeClient()

            # Handle email writing exercise actions
            if action == 'generate':
                return self._handle_generate_letter(data, user_context, session_data)
            elif action == 'evaluate':
                return self._handle_evaluate_response(data, user_context, session_data)
            else:
                return False, {'error': f'Unknown action: {action}'}

        except Exception as e:
            print(f"[ERROR] [EXERCISE MANAGER] Error processing request: {e}")
            import traceback
            print(f"[ERROR] [EXERCISE MANAGER] Traceback: {traceback.format_exc()}")
            return False, {'error': str(e)}

    def _handle_generate_letter(self, data: dict, user_context: dict,
                                session_data: dict) -> Tuple[bool, dict]:
        """Generate a letter for the email writing exercise."""
        try:
            # Get user information for personalization
            user_name = "Student"
            user_level = "intermediate"

            if user_context and user_context.get('user_id'):
                # Try to get user info from database
                try:
                    from database import db

                    user = db.session.query(User).filter_by(
                        id=user_context['user_id']
                    ).first()

                    if user:
                        user_name = user.email.split('@')[0]  # Use email prefix as name
                        # In Spralingua, we can use the progress_level or default to intermediate
                        user_level = user_context.get('level', 'intermediate')
                except Exception as e:
                    print(f"[WARNING] [EXERCISE MANAGER] Could not retrieve user info: {e}")

            # Get level-specific configuration
            level_config = self.prompt_manager.get_prompt('level_configs', {}).get(
                user_level,
                self.prompt_manager.get_prompt('level_configs', {}).get('intermediate', {})
            )

            # Simple topic selection for Spralingua
            topics = [
                {'name': 'Travel & Vacation', 'instruction': 'planning a trip or vacation'},
                {'name': 'Work & Studies', 'instruction': 'discussing work or study experiences'},
                {'name': 'Lifestyle Changes', 'instruction': 'talking about daily routine changes'},
                {'name': 'Family News', 'instruction': 'sharing family events and news'},
                {'name': 'Hobbies', 'instruction': 'discussing hobbies and free time activities'}
            ]
            topic = random.choice(topics)
            topic_instruction = f"Write about {topic['instruction']}"

            print(f"[INFO] [EXERCISE MANAGER] Selected topic: {topic['name']} for {user_name} (level: {user_level})")

            # Build the generation prompt
            generation_prompt = self.prompt_manager.get_prompt('exercise_generation_prompt', '')

            # Substitute placeholders
            generation_prompt = generation_prompt.replace('{student_name}', user_name)
            generation_prompt = generation_prompt.replace('{student_level}', user_level)
            generation_prompt = generation_prompt.replace('{topic_instruction}', topic_instruction)
            generation_prompt = generation_prompt.replace('{word_count}', level_config.get('word_count', '100-150'))
            generation_prompt = generation_prompt.replace('{level_description}', level_config.get('level_description', 'B1-B2 level'))
            generation_prompt = generation_prompt.replace('{level_specific_requirements}', level_config.get('requirements', ''))

            # Get Claude to generate the letter
            response = self.claude_client.send_message(
                user_input="Generate an email writing exercise for me.",
                system_prompt=generation_prompt
            )

            # Parse the full exercise from the response
            # Try to extract letter and response prompts
            letter = ""
            response_prompts = []

            # Look for the letter between backticks
            letter_match = re.search(r'```\n(.*?)\n```', response, re.DOTALL)
            if letter_match:
                letter = letter_match.group(1).strip()

            # Look for response prompts (bullet points after the letter)
            prompts_section = re.search(r'Antworten Sie.*?:\s*((?:•.*?\n)+)', response, re.DOTALL)
            if prompts_section:
                prompts_text = prompts_section.group(1)
                # Extract each bullet point
                prompts = re.findall(r'•\s*(.+?)(?:\n|$)', prompts_text)
                response_prompts = [prompt.strip() for prompt in prompts if prompt.strip()]

            # If we couldn't parse properly, use the whole response as the letter
            if not letter:
                letter = response

            # If we didn't find prompts, use default ones
            if not response_prompts:
                response_prompts = [
                    "Reaktion auf die Nachricht",
                    "Persönliche Erfahrung oder Meinung",
                    "Ratschlag oder Vorschlag",
                    "Zukunftspläne oder Fragen"
                ]

            # Store the generated letter in session data
            if session_data is not None:
                session_data['generated_letter'] = response  # Store full response
                session_data['parsed_letter'] = letter  # Store just the letter part
                session_data['user_level'] = user_level
                session_data['selected_topic'] = topic['name']  # Store selected topic

            # Extract word count range
            word_count_range = level_config.get('word_count', '100-150')
            # Get the upper limit for the word count (e.g., "100-150" -> 150)
            word_limit = int(word_count_range.split('-')[1]) if '-' in word_count_range else 150

            return True, {
                'letter': letter,
                'response_prompts': response_prompts,
                'expected_length': level_config.get('expected_response_length', 250),
                'word_limit': word_limit,
                'word_count_range': word_count_range,
                'topic': topic['name'],  # Include topic in response
                'attempt': 1
            }

        except Exception as e:
            print(f"[ERROR] [EXERCISE MANAGER] Error generating letter: {e}")
            return False, {'error': f'Failed to generate letter: {str(e)}'}

    def _handle_evaluate_response(self, data: dict, user_context: dict,
                                  session_data: dict) -> Tuple[bool, dict]:
        """Evaluate the student's response."""
        try:
            attempt = data.get('attempt', 1)
            student_response = data.get('body', '')
            original_letter = session_data.get('generated_letter', '') if session_data else ''
            user_level = session_data.get('user_level', 'intermediate') if session_data else 'intermediate'

            if not student_response:
                return False, {'error': 'No response provided'}

            if attempt == 1:
                # First attempt - identify errors
                evaluation_prompt = self.prompt_manager.get_prompt('evaluation_prompt_attempt1', '')

                # Substitute placeholders
                evaluation_prompt = evaluation_prompt.replace('{student_level}', user_level)
                evaluation_prompt = evaluation_prompt.replace('{original_letter}', original_letter)
                evaluation_prompt = evaluation_prompt.replace('{student_response}', student_response)

                # Get Claude to evaluate
                response = self.claude_client.send_message(
                    user_input="Evaluate this German response and identify errors.",
                    system_prompt=evaluation_prompt
                )

                # Parse JSON response
                json_response = self._extract_json_from_response(response)
                if json_response:
                    # Store first attempt for second evaluation
                    if session_data is not None:
                        session_data['first_attempt'] = student_response
                    return True, json_response
                else:
                    # Fallback response
                    return True, {
                        'errors': [],
                        'message': 'Unable to analyze errors. Please proceed to attempt 2.',
                        'general_feedback': 'Keep trying!'
                    }

            else:  # attempt == 2
                # Second attempt - full feedback
                evaluation_prompt = self.prompt_manager.get_prompt('evaluation_prompt_attempt2', '')
                first_attempt = session_data.get('first_attempt', '') if session_data else ''

                # Substitute placeholders
                evaluation_prompt = evaluation_prompt.replace('{student_level}', user_level)
                evaluation_prompt = evaluation_prompt.replace('{original_letter}', original_letter)
                evaluation_prompt = evaluation_prompt.replace('{first_attempt}', first_attempt)
                evaluation_prompt = evaluation_prompt.replace('{second_attempt}', student_response)

                # Get Claude to provide full feedback
                response = self.claude_client.send_message(
                    user_input="Provide comprehensive feedback on this German response.",
                    system_prompt=evaluation_prompt
                )

                # Parse JSON response
                json_response = self._extract_json_from_response(response)
                if json_response:
                    return True, json_response
                else:
                    # Fallback response
                    return True, {
                        'original_text': student_response,
                        'corrected_text': student_response,
                        'explanations': [],
                        'focus_points': ['Keep practicing!', 'Review grammar rules'],
                        'score': 70,
                        'feedback': 'Good effort! Keep practicing your German writing.',
                        'improvements_from_first': 'You made some improvements.'
                    }

        except Exception as e:
            print(f"[ERROR] [EXERCISE MANAGER] Error evaluating response: {e}")
            return False, {'error': f'Failed to evaluate response: {str(e)}'}

    def _extract_json_from_response(self, response: str) -> Optional[dict]:
        """Extract JSON from Claude's response."""
        try:
            json_str = None

            # Method 1: Try to find JSON wrapped in ```json``` markers
            json_code_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_code_match:
                json_str = json_code_match.group(1).strip()
                print(f"[DEBUG] [EXERCISE MANAGER] Found JSON in code block")

            # Method 2: Try to find JSON object starting with { and ending with }
            elif response.strip().startswith('{') and response.strip().endswith('}'):
                json_str = response.strip()
                print(f"[DEBUG] [EXERCISE MANAGER] Using entire response as JSON")

            # Method 3: Look for JSON object in the middle of text
            else:
                # Find the first { and last } to extract the JSON object
                start_idx = response.find('{')
                end_idx = response.rfind('}')

                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx + 1]
                    print(f"[DEBUG] [EXERCISE MANAGER] Extracted JSON from position {start_idx} to {end_idx}")
                else:
                    print(f"[ERROR] [EXERCISE MANAGER] No valid JSON structure found in response")
                    return None

            if not json_str:
                print(f"[ERROR] [EXERCISE MANAGER] No JSON string extracted")
                return None

            # Clean up the JSON string - remove problematic control characters
            json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', json_str)

            # Try to parse the JSON
            try:
                result = json.loads(json_str)
                print(f"[DEBUG] [EXERCISE MANAGER] Successfully parsed JSON")
                return result
            except json.JSONDecodeError as e:
                print(f"[ERROR] [EXERCISE MANAGER] JSON parsing failed: {e}")
                # Try to fix common JSON issues
                # Remove trailing commas
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)

                try:
                    result = json.loads(json_str)
                    print(f"[DEBUG] [EXERCISE MANAGER] Successfully parsed JSON after cleanup")
                    return result
                except:
                    print(f"[ERROR] [EXERCISE MANAGER] Could not fix JSON")
                    return None

        except Exception as e:
            print(f"[ERROR] [EXERCISE MANAGER] Unexpected error extracting JSON: {e}")
            return None