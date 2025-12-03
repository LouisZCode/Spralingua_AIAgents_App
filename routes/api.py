"""
API routes blueprint.
Handles all /api/* endpoints.
"""

import time
import uuid
import os
from flask import Blueprint, request, jsonify, session, current_app

from auth.decorators import login_required
from progress.progress_manager import ProgressManager


api_bp = Blueprint('api', __name__)


# =============================================================================
# Test Routes
# =============================================================================

@api_bp.route('/test-claude', methods=['GET'])
def test_claude():
    """Test Claude API connection."""
    try:
        from services.claude_client import ClaudeClient

        claude = ClaudeClient()
        response = claude.send_message(
            "Say 'Hello! Claude is working!' in German.",
            "You are a helpful assistant. Respond briefly."
        )

        return jsonify({
            'success': True,
            'response': response,
            'message': 'Claude API is connected!'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to connect to Claude API'
        }), 500


# =============================================================================
# Casual Chat Routes
# =============================================================================

@api_bp.route('/casual-chat/chat', methods=['POST'])
@login_required
def casual_chat():
    """Chat API endpoint for casual chat conversation practice."""
    try:
        from services.claude_client import ClaudeClient
        from prompts.prompt_manager import PromptManager
        from services.feedback import generate_language_hint, generate_comprehensive_feedback

        # Get request data
        data = request.get_json()
        message = data.get('message', '')
        character = data.get('character', 'harry')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Log worker process info for debugging
        worker_pid = os.getpid()
        print(f"[WORKER DEBUG] Process ID: {worker_pid}")

        # Initialize or get Claude client
        if 'claude_client' not in session:
            session['claude_client'] = True
            claude = ClaudeClient()
            print(f"[WORKER DEBUG] Created NEW ClaudeClient in worker {worker_pid}")
            current_app.claude_clients = getattr(current_app, 'claude_clients', {})
            session_id = session.get('_id', id(session))
            current_app.claude_clients[session_id] = claude
        else:
            current_app.claude_clients = getattr(current_app, 'claude_clients', {})
            session_id = session.get('_id', id(session))
            if session_id not in current_app.claude_clients:
                claude = ClaudeClient()
                current_app.claude_clients[session_id] = claude
            else:
                claude = current_app.claude_clients[session_id]

        # Restore conversation history from session (survives across workers)
        if 'claude_conversation_history' in session:
            claude.set_conversation_history(session['claude_conversation_history'])
            print(f"[SESSION RESTORE] Restored {len(session['claude_conversation_history'])} messages")

        # Build dynamic prompt
        system_prompt = None
        user_context = {}

        if 'user_id' in session:
            try:
                from prompts.conversation_prompt_builder import ConversationPromptBuilder
                prompt_builder = ConversationPromptBuilder()
                topic_override = session.get('exercise_topic')

                dynamic_prompt, context = prompt_builder.build_prompt(
                    session['user_id'],
                    character,
                    topic_override=topic_override
                )

                if dynamic_prompt:
                    system_prompt = dynamic_prompt
                    user_context = context
                    print(f"[INFO] Using dynamic prompt for user {session['user_id']}")

            except Exception as e:
                print(f"[WARNING] Dynamic prompt failed: {e}")

        # Fallback to error prompt
        if not system_prompt:
            prompt_file = os.path.join('prompts', 'fallback_error.yaml')
            prompt_manager = PromptManager(prompt_file)
            system_prompt = prompt_manager.get_prompt('casual_chat_prompt', '')
            print(f"[WARNING] Using fallback ERROR prompt")

        # Track messages and scoring
        if 'casual_chat_messages' not in session:
            session['casual_chat_messages'] = []
        if 'casual_chat_correct' not in session:
            session['casual_chat_correct'] = 0
            session['casual_chat_total'] = 0

        session['casual_chat_messages'].append(message)
        message_count = len(session['casual_chat_messages'])
        session['casual_chat_total'] = message_count

        # Send message to Claude
        response = claude.send_message(message, system_prompt)

        # Save conversation history to session
        session['claude_conversation_history'] = claude.get_conversation_history()

        # Add delay to prevent context bleeding
        time.sleep(0.5)

        # Get number of exchanges from context
        total_exchanges = user_context.get('number_of_exchanges', 5)

        # Prepare response data
        response_data = {
            'response': response,
            'message_count': message_count,
            'total_messages_required': total_exchanges
        }

        feedback_level = user_context.get('level', 'A1').upper()

        # Generate hint for each message except the last
        if message_count < total_exchanges:
            target_language = user_context.get('target_language', 'german')
            native_language = user_context.get('input_language', 'english')

            hint_data = generate_language_hint(
                message, claude, feedback_level,
                target_language=target_language,
                native_language=native_language
            )

            if hint_data and 'type' in hint_data:
                type_mapping = {'correction': 'error', 'hint': 'warning', 'suggestion': 'warning', 'tip': 'warning'}
                hint_data['type'] = type_mapping.get(hint_data['type'], hint_data['type'])
                if hint_data['type'] in ['praise', 'warning']:
                    session['casual_chat_correct'] += 1

            response_data['hint'] = hint_data

        # Generate comprehensive feedback at last message
        if message_count == total_exchanges:
            target_language = user_context.get('target_language', 'german')
            native_language = user_context.get('input_language', 'english')

            feedback_data = generate_comprehensive_feedback(
                session['casual_chat_messages'], claude, feedback_level,
                target_language=target_language,
                native_language=native_language
            )
            response_data['comprehensive_feedback'] = feedback_data

        # Mark as complete and save score
        if message_count >= total_exchanges:
            response_data['module_completed'] = True

            if session['casual_chat_total'] > 0:
                score = (session['casual_chat_correct'] / session['casual_chat_total']) * 100

                if 'user_id' in session:
                    try:
                        from progress.exercise_progress_manager import ExerciseProgressManager

                        progress_manager = ProgressManager()
                        input_lang = user_context.get('input_language', 'english')
                        target_lang = user_context.get('target_language', 'german')

                        user_progress = progress_manager.get_user_progress(
                            session['user_id'], input_lang, target_lang
                        )

                        if user_progress:
                            exercise_manager = ExerciseProgressManager()
                            result = exercise_manager.record_exercise_attempt(
                                user_progress_id=user_progress.id,
                                level=user_progress.current_level,
                                topic_number=user_progress.current_topic,
                                exercise_type='casual_chat',
                                score=score,
                                messages_correct=session['casual_chat_correct'],
                                messages_total=session['casual_chat_total']
                            )

                            response_data['score'] = score
                            response_data['messages_correct'] = session['casual_chat_correct']
                            response_data['messages_total'] = session['casual_chat_total']
                            response_data['exercise_completed'] = result.get('newly_completed', False)
                            response_data['topic_advanced'] = result.get('topic_advanced', False)

                            print(f"[SCORE SAVED] Casual Chat: {score:.1f}%")
                    except Exception as e:
                        print(f"[ERROR] Saving exercise score: {e}")

            # Clear session for next conversation
            session['casual_chat_messages'] = []
            session['casual_chat_correct'] = 0
            session['casual_chat_total'] = 0

        session.modified = True
        return jsonify(response_data)

    except Exception as e:
        print(f"[ERROR] Casual chat API: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/casual-chat/clear', methods=['POST'])
@login_required
def clear_casual_chat():
    """Clear casual chat conversation history."""
    try:
        if 'casual_chat_messages' in session:
            session['casual_chat_messages'] = []
        if 'casual_chat_correct' in session:
            session['casual_chat_correct'] = 0
        if 'casual_chat_total' in session:
            session['casual_chat_total'] = 0
        if 'claude_client' in session:
            session.pop('claude_client', None)
        if 'claude_conversation_history' in session:
            session.pop('claude_conversation_history', None)
            print("[SESSION CLEAR] Cleared conversation history")

        if hasattr(current_app, 'claude_clients'):
            current_app.claude_clients = {}

        session.modified = True
        return jsonify({'status': 'success', 'message': 'Conversation cleared'})

    except Exception as e:
        print(f"[ERROR] Clearing conversation: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/casual-chat/tts', methods=['POST'])
@login_required
def casual_chat_tts():
    """Text-to-speech endpoint for casual chat using Minimax."""
    try:
        from services.minimax_client import minimax_client

        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400

        text = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400

        character = data.get('character')
        voice_id = data.get('voice_id')
        speed = data.get('speed')
        volume = data.get('vol')
        pitch = data.get('pitch')

        print(f"[TTS REQUEST] Character: {character}, Text length: {len(text)}")

        success, result = minimax_client.synthesize_speech(
            text=text,
            character=character,
            voice_id=voice_id,
            speed=speed,
            volume=volume,
            pitch=pitch
        )

        if success:
            return jsonify(result)
        else:
            return jsonify(result), 500

    except Exception as e:
        print(f"[ERROR] TTS endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/casual-chat/scenario', methods=['GET'])
@login_required
def get_chat_scenario():
    """Get dynamic scenario for current user's topic and language pair."""
    try:
        from scenarios.scenario_manager import ScenarioManager

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        character = request.args.get('character', 'harry')
        topic_override = session.get('exercise_topic')

        scenario_manager = ScenarioManager()
        scenario_text, context = scenario_manager.get_scenario_for_user(user_id, character, topic_override)

        return jsonify({
            'scenario': scenario_text,
            'context': context,
            'status': 'success'
        })

    except Exception as e:
        print(f"[ERROR] Fetching scenario: {e}")
        return jsonify({'error': str(e)}), 500


# =============================================================================
# User Progress Routes
# =============================================================================

@api_bp.route('/user-progress', methods=['GET'])
@login_required
def get_user_progress():
    """Get current user's progress for the active language pair."""
    try:
        from progress.exercise_progress_manager import ExerciseProgressManager
        from topics.topic_manager import TopicManager
        from tests.test_manager import TestManager

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        input_lang = request.args.get('input_language')
        target_lang = request.args.get('target_language')

        progress_manager = ProgressManager()
        exercise_manager = ExerciseProgressManager()
        topic_manager = TopicManager()
        test_manager = TestManager()

        user_progress = progress_manager.get_user_progress(user_id, input_lang, target_lang)

        if not user_progress:
            return jsonify({'error': 'No progress found for this language pair'}), 404

        topics = topic_manager.get_all_topics_for_level(user_progress.current_level)
        all_topic_progress = topic_manager.get_user_topic_progress(user_progress.id, user_progress.current_level)

        topic_progress_list = []
        completed_topics = []

        completed_topics_nums = [tp.topic_number for tp in all_topic_progress if tp.completed]
        max_accessible_topic = max(completed_topics_nums) + 1 if completed_topics_nums else user_progress.current_topic

        for topic in topics:
            topic_progress = next((tp for tp in all_topic_progress if tp.topic_number == topic.topic_number), None)
            exercise_status = exercise_manager.get_topic_exercises_status(
                user_progress.id, user_progress.current_level, topic.topic_number
            )

            is_completed = topic_progress.completed if topic_progress else False
            is_current = (topic.topic_number == user_progress.current_topic)
            is_locked = topic.topic_number > max_accessible_topic

            if is_completed:
                completed_topics.append(topic.topic_number)

            topic_progress_list.append({
                'topic_number': topic.topic_number,
                'title': topic.title_key,
                'completed': is_completed,
                'current': is_current,
                'locked': is_locked,
                'exercises': exercise_status['exercises']
            })

        # Test progress
        test_progress_list = []
        test_configs = [
            {'type': 'checkpoint_1', 'after_topic': 3, 'number': 1},
            {'type': 'checkpoint_2', 'after_topic': 6, 'number': 2},
            {'type': 'checkpoint_3', 'after_topic': 9, 'number': 3},
            {'type': 'final', 'after_topic': 12, 'number': 4}
        ]

        for test_config in test_configs:
            test_progress = test_manager.get_test_progress(user_progress.id, test_config['type'])
            required_topics = list(range(test_config['after_topic'] - 2, test_config['after_topic'] + 1))
            is_unlocked = all(t in completed_topics for t in required_topics)

            test_progress_list.append({
                'test_number': test_config['number'],
                'test_type': test_config['type'],
                'after_topic': test_config['after_topic'],
                'unlocked': is_unlocked,
                'passed': test_progress.passed if test_progress else False,
                'attempts': test_progress.attempts if test_progress else 0,
                'score': test_progress.score if test_progress else None
            })

        # Calculate overall progress
        total_points = 16
        completed_points = len(completed_topics)
        for test in test_progress_list:
            if test['passed']:
                completed_points += 1
        overall_progress = int((completed_points / total_points) * 100)

        return jsonify({
            'current_level': user_progress.current_level,
            'current_topic': user_progress.current_topic,
            'overall_progress': overall_progress,
            'completed_points': completed_points,
            'total_points': total_points,
            'topics': topic_progress_list,
            'tests': test_progress_list,
            'input_language': user_progress.input_language,
            'target_language': user_progress.target_language
        })

    except Exception as e:
        print(f"[ERROR] Getting user progress: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/check-completion-popup', methods=['GET'])
@login_required
def check_completion_popup():
    """Check if a completion popup should be shown for the current topic."""
    try:
        from topics.topic_manager import TopicManager

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        input_lang = request.args.get('input_language')
        target_lang = request.args.get('target_language')

        if not input_lang or not target_lang:
            return jsonify({'show_popup': False}), 200

        progress_mgr = ProgressManager()
        user_progress = progress_mgr.get_or_create_progress(user_id, input_lang, target_lang)

        if not user_progress:
            return jsonify({'show_popup': False}), 200

        topic_mgr = TopicManager()
        popup_info = topic_mgr.check_completion_popup_needed(user_progress.id)

        if popup_info:
            return jsonify(popup_info), 200
        else:
            return jsonify({'show_popup': False}), 200

    except Exception as e:
        print(f"[ERROR] Checking completion popup: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/mark-popup-seen', methods=['POST'])
@login_required
def mark_popup_seen():
    """Mark that the completion popup has been shown for a topic."""
    try:
        from topics.topic_manager import TopicManager

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        data = request.get_json()
        topic_number = data.get('topic_number')
        input_lang = data.get('input_language')
        target_lang = data.get('target_language')

        if not all([topic_number, input_lang, target_lang]):
            return jsonify({'error': 'Missing required fields'}), 400

        progress_mgr = ProgressManager()
        user_progress = progress_mgr.get_or_create_progress(user_id, input_lang, target_lang)

        if not user_progress:
            return jsonify({'error': 'User progress not found'}), 404

        topic_mgr = TopicManager()
        success, message = topic_mgr.mark_popup_seen(user_progress.id, topic_number)

        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'error': message}), 400

    except Exception as e:
        print(f"[ERROR] Marking popup seen: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/navigate-to-topic', methods=['POST'])
@login_required
def navigate_to_topic():
    """Navigate to a different topic."""
    try:
        from topics.topic_manager import TopicManager

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        data = request.get_json()
        new_topic = data.get('topic_number')
        input_lang = data.get('input_language')
        target_lang = data.get('target_language')

        if not all([new_topic, input_lang, target_lang]):
            return jsonify({'error': 'Missing required fields'}), 400

        progress_mgr = ProgressManager()
        user_progress = progress_mgr.get_or_create_progress(user_id, input_lang, target_lang)

        if not user_progress:
            return jsonify({'error': 'User progress not found'}), 404

        topic_mgr = TopicManager()
        success, result = topic_mgr.navigate_to_topic(user_progress.id, new_topic)

        if success:
            return jsonify({'success': True, **result}), 200
        else:
            return jsonify({'error': result.get('error', 'Navigation failed')}), 400

    except Exception as e:
        print(f"[ERROR] Navigating to topic: {e}")
        return jsonify({'error': str(e)}), 500


# =============================================================================
# Email Writing Routes
# =============================================================================

@api_bp.route('/writing-practice/generate', methods=['POST'])
@login_required
def generate_email_letter():
    """Generate a letter for the email writing exercise."""
    try:
        from email_writing.exercise_manager import EmailExerciseManager

        user_id = session.get('user_id')
        topic_override = session.get('exercise_topic')

        user_context = {
            'user_id': user_id,
            'topic_override': topic_override
        }

        # Get or create session ID
        session_id = session.get('email_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['email_session_id'] = session_id

        exercise_session_key = f'email_writing_{session_id}'
        if exercise_session_key not in session:
            session[exercise_session_key] = {}
        session_data = session[exercise_session_key]

        exercise_manager = EmailExerciseManager()

        success, result = exercise_manager.process_exercise_request(
            action='generate',
            data={},
            user_context=user_context,
            session_data=session_data
        )

        session[exercise_session_key] = session_data
        session.modified = True

        if success:
            return jsonify(result)
        else:
            return jsonify(result), 500

    except Exception as e:
        print(f"[ERROR] Generating letter: {e}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to generate letter: {str(e)}'}), 500


@api_bp.route('/writing-practice/submit', methods=['POST'])
@login_required
def submit_email_response():
    """Submit and evaluate a response for the email writing exercise."""
    try:
        from email_writing.exercise_manager import EmailExerciseManager

        user_id = session.get('user_id')
        user_context = {'user_id': user_id, 'level': 'intermediate'}

        session_id = session.get('email_session_id', 'default')
        exercise_session_key = f'email_writing_{session_id}'
        session_data = session.get(exercise_session_key, {})

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        exercise_manager = EmailExerciseManager()

        success, result = exercise_manager.process_exercise_request(
            action='evaluate',
            data=data,
            user_context=user_context,
            session_data=session_data
        )

        session[exercise_session_key] = session_data
        session.modified = True

        if success:
            # Save score if comprehensive feedback
            if result.get('feedback_type') == 'comprehensive' and 'score' in result:
                try:
                    from progress.exercise_progress_manager import ExerciseProgressManager

                    progress_manager = ProgressManager()

                    stored_context = session_data.get('user_context')
                    if stored_context:
                        input_lang = stored_context.get('input_language', 'english')
                        target_lang = stored_context.get('target_language', 'german')
                    else:
                        input_lang = session_data.get('native_language', 'english')
                        target_lang = session_data.get('target_language', 'german')

                    user_progress = progress_manager.get_user_progress(user_id, input_lang, target_lang)

                    if user_progress:
                        topic_number = session.get('exercise_topic', user_progress.current_topic)

                        exercise_manager_db = ExerciseProgressManager()
                        db_result = exercise_manager_db.record_exercise_attempt(
                            user_progress_id=user_progress.id,
                            level=user_progress.current_level,
                            topic_number=topic_number,
                            exercise_type='email_writing',
                            score=result['score']
                        )

                        result['exercise_completed'] = db_result.get('newly_completed', False)
                        result['topic_advanced'] = db_result.get('topic_advanced', False)

                        print(f"[SCORE SAVED] Email Writing: {result['score']}%")

                except Exception as e:
                    print(f"[ERROR] Saving email writing score: {e}")

            return jsonify(result)
        else:
            return jsonify(result), 500

    except Exception as e:
        print(f"[ERROR] Evaluating response: {e}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to evaluate response: {str(e)}'}), 500
