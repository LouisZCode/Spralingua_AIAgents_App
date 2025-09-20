"""Email Exercise manager for Spralingua."""

import json
import re
import random
from typing import Dict, Any, Optional, Tuple
from claude_client import ClaudeClient
from models.user import User
from email_writing.email_prompt_builder import EmailPromptBuilder
from email_writing.email_feedback_builder import EmailFeedbackBuilder
from email_writing.letter_templates import LetterTemplates


class EmailExerciseManager:
    """Manages email writing exercise logic and AI interactions."""

    def __init__(self):
        """
        Initialize the exercise manager.
        """
        self.prompt_builder = EmailPromptBuilder()
        self.feedback_builder = EmailFeedbackBuilder()
        self.letter_templates = LetterTemplates()
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
            user_id = user_context.get('user_id')

            if user_id:
                # Try to get user info from database
                try:
                    from database import db
                    user = db.session.query(User).filter_by(id=user_id).first()
                    if user:
                        user_name = user.name  # Use real name from database
                except Exception as e:
                    print(f"[WARNING] [EXERCISE MANAGER] Could not retrieve user info: {e}")

            # Get topic override from user context if available
            topic_override = user_context.get('topic_override')
            if topic_override:
                print(f"[INFO] [EXERCISE MANAGER] Using topic override: {topic_override}")

            # Build the generation prompt using the new language-aware builder
            print(f"[DEBUG] [EXERCISE MANAGER] Building generation prompt for user_id: {user_id}")
            generation_prompt, context = self.prompt_builder.build_generation_prompt(user_id, topic_override)
            print(f"[DEBUG] [EXERCISE MANAGER] Got prompt: {bool(generation_prompt)}, context: {bool(context)}")

            if not generation_prompt or not context:
                print(f"[ERROR] [EXERCISE MANAGER] Could not build generation prompt for user {user_id}")
                print(f"[ERROR] [EXERCISE MANAGER] Returning error response")
                # Return error response directly - no fallback to German
                return True, {
                    'letter': 'ERROR - System configuration issue. The dynamic prompt system failed. Please contact support.',
                    'response_prompts': ['System error occurred - Unable to generate exercise'],
                    'expected_length': 0,
                    'word_limit': 0,
                    'word_count_range': '0-0',
                    'topic': 'ERROR',
                    'target_language': 'unknown',
                    'native_language': 'unknown',
                    'attempt': 1
                }

            print(f"[INFO] [EXERCISE MANAGER] Generating letter for {user_name}")
            print(f"[INFO] [EXERCISE MANAGER] Language: {context['input_language']} -> {context['target_language']}")
            print(f"[INFO] [EXERCISE MANAGER] Level: {context['level']}, Topic {context['topic_number']}: {context['topic_title']}")

            # Get Claude to generate the letter
            response = self.claude_client.send_message(
                user_input="Generate an email writing exercise for me.",
                system_prompt=generation_prompt
            )

            # Parse the letter using the letter templates parser
            letter_data = self.letter_templates.parse_letter_response(
                response,
                context['target_language']
            )

            # Get culturally appropriate response prompts in user's native language
            response_prompts = self.feedback_builder.get_response_prompts(
                context['topic_number'],
                context['input_language']  # Native language for instructions
            )

            # Only use Claude's prompts if we don't have proper translations
            if not response_prompts and letter_data['response_prompts']:
                response_prompts = letter_data['response_prompts']

            # Format the letter for display
            formatted_letter = self.letter_templates.format_letter_for_display(
                letter_data,
                user_name
            )

            # Store the generated letter and context in session
            if session_data is not None:
                session_data['generated_letter'] = response  # Store full response
                session_data['parsed_letter'] = letter_data['letter']
                session_data['user_context'] = context  # Store full context
                session_data['target_language'] = context['target_language']
                session_data['native_language'] = context['input_language']

            # Determine word limit based on level
            word_limits = {
                'A1': 50,
                'A2': 80,
                'B1': 120,
                'B2': 150
            }
            word_limit = word_limits.get(context['level'], 100)
            word_count_range = f"{int(word_limit * 0.8)}-{word_limit}"

            return True, {
                'letter': formatted_letter,
                'response_prompts': response_prompts,
                'expected_length': word_limit,
                'word_limit': word_limit,
                'word_count_range': word_count_range,
                'topic': context['topic_title'],
                'target_language': context['target_language'],
                'native_language': context['input_language'],
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

            # Get stored context from session
            stored_context = session_data.get('user_context') if session_data else None

            if not stored_context:
                print(f"[ERROR] [EXERCISE MANAGER] No stored context for evaluation")
                # Return error response directly - no fallback
                return True, {
                    'errors': [],
                    'message': 'ERROR - System configuration issue. Unable to evaluate response.',
                    'general_feedback': 'Please try regenerating the exercise.'
                }

            if not student_response:
                return False, {'error': 'No response provided'}

            if attempt == 1:
                # First attempt - build evaluation prompt with language context
                evaluation_prompt = self.prompt_builder.build_evaluation_prompt(
                    stored_context,
                    attempt=1,
                    original_letter=original_letter,
                    student_response=student_response
                )

                # Get Claude to evaluate
                target_lang = stored_context['target_language'].capitalize()
                response = self.claude_client.send_message(
                    user_input=f"Evaluate this {target_lang} response and identify errors.",
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
                # Second attempt - full feedback with language context
                first_attempt = session_data.get('first_attempt', '') if session_data else ''

                evaluation_prompt = self.prompt_builder.build_evaluation_prompt(
                    stored_context,
                    attempt=2,
                    original_letter=original_letter,
                    student_response=student_response,
                    first_attempt=first_attempt
                )

                # Get Claude to provide full feedback
                target_lang = stored_context['target_language'].capitalize()
                response = self.claude_client.send_message(
                    user_input=f"Provide comprehensive feedback on this {target_lang} response.",
                    system_prompt=evaluation_prompt
                )

                # Parse JSON response
                json_response = self._extract_json_from_response(response)
                if json_response:
                    # Add feedback_type for score saving
                    json_response['feedback_type'] = 'comprehensive'
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
                        'improvements_from_first': 'You made some improvements.',
                        'feedback_type': 'comprehensive'  # Required for score saving
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

