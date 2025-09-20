# Authentication Routes for Spralingua

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .auth_manager import AuthManager
from .decorators import login_required, guest_only
from progress.progress_manager import ProgressManager
import time

class LoginForm(FlaskForm):
    """Login form with CSRF protection."""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Registration form with CSRF protection."""
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class AuthRoutes:
    """Manages authentication routes for the platform."""
    
    def __init__(self, app: Flask, auth_manager: AuthManager):
        """
        Initialize authentication routes.
        
        Args:
            app: Flask application instance
            auth_manager: AuthManager instance
        """
        self.app = app
        self.auth_manager = auth_manager
        self._register_routes()
    
    def _register_routes(self):
        """Register all authentication routes."""
        
        @self.app.route('/login', methods=['GET', 'POST'])
        @guest_only
        def auth_login():
            """Login page and handler."""
            form = LoginForm()
            
            if form.validate_on_submit():
                email = form.email.data
                password = form.password.data
                remember_me = form.remember_me.data
                
                # Authenticate user
                success, user = self.auth_manager.authenticate_user(email, password)
                
                if success and user:
                    # Log in the user
                    self.auth_manager.login_user(user, session)
                    
                    # Set session as permanent if remember me is checked
                    if remember_me:
                        session.permanent = True
                    
                    # Redirect to next URL or dashboard
                    next_url = session.pop('next_url', None)
                    if next_url:
                        return redirect(next_url)
                    
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password', 'error')
            
            return render_template('auth/login.html', form=form)
        
        @self.app.route('/register', methods=['GET', 'POST'])
        @guest_only
        def auth_register():
            """Registration page and handler."""
            form = RegistrationForm()
            
            if form.validate_on_submit():
                name = form.name.data
                email = form.email.data
                password = form.password.data
                
                # Register user with name
                success, result = self.auth_manager.register_user(email, name, password)
                
                if success:
                    # Log the user in automatically
                    user = result.get('user')
                    self.auth_manager.login_user(user, session)
                    
                    flash(f'Registration successful! Welcome to Spralingua, {user.name}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    error_msg = result.get('error', 'Registration failed')
                    flash(error_msg, 'error')
            
            return render_template('auth/register.html', form=form)
        
        @self.app.route('/logout')
        @login_required
        def auth_logout():
            """Logout handler."""
            self.auth_manager.logout_user(session)
            flash('You have been logged out successfully.', 'info')
            return redirect(url_for('landing'))
        
        @self.app.route('/dashboard')
        @login_required
        def dashboard():
            """Dashboard page for logged-in users."""
            from progress.progress_manager import ProgressManager
            
            email = session.get('email', 'User')
            user_id = session.get('user_id')
            
            # Get user's most recent progress
            progress_mgr = ProgressManager()
            user_progress = progress_mgr.get_user_progress(user_id) if user_id else None
            
            # Prepare progress data for template
            progress_data = None
            if user_progress:
                progress_data = {
                    'input_language': user_progress.input_language,
                    'target_language': user_progress.target_language,
                    'current_level': user_progress.current_level
                }
            
            return render_template('dashboard.html', 
                                 email=email,
                                 user_progress=progress_data)
        
        @self.app.route('/exercises')
        @login_required
        def exercises():
            """Exercises page for practicing languages."""
            from progress.progress_manager import ProgressManager
            
            email = session.get('email', 'User')
            user_id = session.get('user_id')
            
            # Get user's most recent progress to know what they're learning
            progress_mgr = ProgressManager()
            user_progress = progress_mgr.get_user_progress(user_id) if user_id else None
            
            # Prepare progress data for template
            progress_data = None
            if user_progress:
                progress_data = {
                    'input_language': user_progress.input_language,
                    'target_language': user_progress.target_language,
                    'current_level': user_progress.current_level,
                    'progress_in_level': user_progress.progress_in_level
                }
            
            return render_template('exercises.html', 
                                 email=email,
                                 user_progress=progress_data)
        
        @self.app.route('/casual-chat')
        @login_required
        def casual_chat():
            """Casual chat conversation practice page."""
            from progress.progress_manager import ProgressManager
            from language.language_mapper import LanguageMapper
            
            email = session.get('email', 'User')
            user_id = session.get('user_id')

            # Get topic override from URL parameter if provided
            topic_override = request.args.get('topic', type=int)
            if topic_override:
                # Store in session for API endpoints to use
                session['exercise_topic'] = topic_override

            # Get user's current language progress
            progress_mgr = ProgressManager()
            user_progress = progress_mgr.get_user_progress(user_id) if user_id else None
            
            # Check if user has selected languages
            if not user_progress:
                flash('Please select your languages first to start practicing!', 'warning')
                return redirect(url_for('dashboard'))
            
            # Map target language to speech recognition code
            target_language = user_progress.target_language
            speech_code = LanguageMapper.get_speech_code(target_language)
            
            # If somehow the language isn't supported, redirect
            if not speech_code:
                flash('Language configuration error. Please select your languages again.', 'error')
                return redirect(url_for('dashboard'))
            
            return render_template('casual_chat.html', 
                                 email=email,
                                 target_language=target_language,
                                 speech_code=speech_code)
        
        @self.app.route('/api/test-claude', methods=['GET'])
        def test_claude():
            """Test Claude API connection."""
            try:
                # Import Claude client
                import os
                from claude_client import ClaudeClient
                from prompt_manager import PromptManager
                
                # Initialize Claude client
                claude = ClaudeClient()
                
                # Test with a simple message
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
        
        @self.app.route('/api/casual-chat/chat', methods=['POST'])
        @login_required
        def casual_chat_api():
            """Chat API endpoint for casual chat conversation practice."""
            try:
                import os
                from claude_client import ClaudeClient
                from prompt_manager import PromptManager
                from feedback_generator import generate_language_hint, generate_comprehensive_feedback
                
                # Get request data
                data = request.get_json()
                message = data.get('message', '')
                character = data.get('character', 'harry')  # Default to Harry
                
                if not message:
                    return jsonify({'error': 'No message provided'}), 400
                
                # Initialize or get Claude client from session
                if 'claude_client' not in session:
                    session['claude_client'] = True
                    # Create new client for this session
                    claude = ClaudeClient()
                    # Store in app context for this request
                    self.app.claude_clients = getattr(self.app, 'claude_clients', {})
                    session_id = session.get('_id', id(session))
                    self.app.claude_clients[session_id] = claude
                else:
                    # Retrieve existing client
                    self.app.claude_clients = getattr(self.app, 'claude_clients', {})
                    session_id = session.get('_id', id(session))
                    if session_id not in self.app.claude_clients:
                        claude = ClaudeClient()
                        self.app.claude_clients[session_id] = claude
                    else:
                        claude = self.app.claude_clients[session_id]
                
                # Feature flag for dynamic prompt system
                USE_DYNAMIC_PROMPTS = True  # Enable new system
                
                system_prompt = None
                user_context = {}
                
                # Try to use dynamic prompt system if enabled and user is logged in
                if USE_DYNAMIC_PROMPTS and 'user_id' in session:
                    try:
                        from prompts.conversation_prompt_builder import ConversationPromptBuilder
                        prompt_builder = ConversationPromptBuilder()

                        # Get topic override from session (set by /casual-chat route)
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
                            print(f"[INFO] Context: {context.get('input_language')} -> {context.get('target_language')}, Level: {context.get('level')}, Topic: {context.get('topic_title')}")
                    except Exception as e:
                        print(f"[WARNING] Dynamic prompt failed, falling back: {e}")
                
                # Fallback to error prompt if dynamic system not available
                if not system_prompt:
                    # Load single fallback error prompt for any character
                    prompt_file = os.path.join('prompts', 'fallback_error.yaml')

                    # Load prompts
                    prompt_manager = PromptManager(prompt_file)
                    system_prompt = prompt_manager.get_prompt('casual_chat_prompt', '')
                    print(f"[WARNING] Using fallback ERROR prompt for character: {character}")
                
                # Track message count and scoring in session
                if 'casual_chat_messages' not in session:
                    session['casual_chat_messages'] = []

                # Initialize message scoring for this session
                if 'casual_chat_correct' not in session:
                    session['casual_chat_correct'] = 0
                    session['casual_chat_total'] = 0

                # Add current message to history
                session['casual_chat_messages'].append(message)
                message_count = len(session['casual_chat_messages'])
                session['casual_chat_total'] = message_count  # Track total messages
                
                # Send message to Claude with character prompt
                response = claude.send_message(message, system_prompt)

                # Add delay to prevent context bleeding between API calls
                time.sleep(0.5)

                # Get number of exchanges from context (dynamic from database)
                total_exchanges = user_context.get('number_of_exchanges', 5)  # Default to 5 if not found

                # Prepare response data
                response_data = {
                    'response': response,
                    'message_count': message_count,
                    'total_messages_required': total_exchanges
                }

                # Determine the level for feedback (from context or default)
                # Use actual database level (A1, A2, B1, B2) instead of generic terms
                feedback_level = user_context.get('level', 'A1').upper()

                # Generate language hint for each message (except the last)
                if message_count < total_exchanges:
                    # Get language pair from user context
                    target_language = user_context.get('target_language', 'german')
                    native_language = user_context.get('input_language', 'english')

                    hint_data = generate_language_hint(
                        message,
                        claude,
                        feedback_level,
                        target_language=target_language,
                        native_language=native_language
                    )

                    # Normalize hint type to ensure frontend recognition
                    if hint_data and 'type' in hint_data:
                        hint_type = hint_data.get('type', 'warning')
                        type_mapping = {
                            'correction': 'error',
                            'hint': 'warning',
                            'suggestion': 'warning',
                            'tip': 'warning'
                        }
                        hint_data['type'] = type_mapping.get(hint_type, hint_type)

                        # Track correctness: 'praise' and 'warning' count as correct, only 'error' is incorrect
                        if hint_data['type'] in ['praise', 'warning']:
                            session['casual_chat_correct'] += 1

                    response_data['hint'] = hint_data
                
                # Generate comprehensive feedback at the last message
                print(f"[FEEDBACK CHECK] Message {message_count} of {total_exchanges} total")
                if message_count == total_exchanges:
                    print(f"[FEEDBACK TRIGGER] Generating comprehensive feedback at FINAL message {message_count}")
                    # Get language pair from user context
                    target_language = user_context.get('target_language', 'german')
                    native_language = user_context.get('input_language', 'english')

                    feedback_data = generate_comprehensive_feedback(
                        session['casual_chat_messages'],
                        claude,
                        feedback_level,
                        target_language=target_language,
                        native_language=native_language
                    )
                    response_data['comprehensive_feedback'] = feedback_data
                    print(f"[FEEDBACK COMPLETE] Added comprehensive feedback to response")
                
                # Mark as complete after reaching the required number of exchanges
                if message_count >= total_exchanges:
                    response_data['module_completed'] = True

                    # Calculate and save the score for this exercise
                    if session['casual_chat_total'] > 0:
                        score = (session['casual_chat_correct'] / session['casual_chat_total']) * 100

                        # Save score using ExerciseProgressManager
                        if 'user_id' in session:
                            try:
                                from progress.exercise_progress_manager import ExerciseProgressManager
                                from progress.progress_manager import ProgressManager

                                # Get user's progress record
                                progress_manager = ProgressManager()
                                user_id = session['user_id']

                                # Get language pair from context
                                input_lang = user_context.get('input_language', 'english')
                                target_lang = user_context.get('target_language', 'german')

                                # Get user progress ID
                                user_progress = progress_manager.get_user_progress(
                                    user_id, input_lang, target_lang
                                )

                                if user_progress:
                                    # Record the exercise attempt
                                    exercise_manager = ExerciseProgressManager()
                                    result = exercise_manager.record_exercise_attempt(
                                        user_progress_id=user_progress.id,
                                        topic_number=user_progress.current_topic,
                                        exercise_type='casual_chat',
                                        score=score,
                                        messages_correct=session['casual_chat_correct'],
                                        messages_total=session['casual_chat_total']
                                    )

                                    # Add score info to response
                                    response_data['score'] = score
                                    response_data['messages_correct'] = session['casual_chat_correct']
                                    response_data['messages_total'] = session['casual_chat_total']
                                    response_data['exercise_completed'] = result.get('newly_completed', False)
                                    response_data['topic_advanced'] = result.get('topic_advanced', False)

                                    print(f"[SCORE SAVED] Casual Chat: {score:.1f}% ({session['casual_chat_correct']}/{session['casual_chat_total']} correct)")
                            except Exception as e:
                                print(f"[ERROR] Saving exercise score: {e}")

                    # Clear session for next conversation
                    session['casual_chat_messages'] = []
                    session['casual_chat_correct'] = 0
                    session['casual_chat_total'] = 0
                
                session.modified = True
                return jsonify(response_data)
                
            except Exception as e:
                print(f"Error in casual chat API: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/casual-chat/clear', methods=['POST'])
        @login_required
        def clear_casual_chat():
            """Clear casual chat conversation history."""
            try:
                # Clear message history
                if 'casual_chat_messages' in session:
                    session['casual_chat_messages'] = []

                # Clear scoring data
                if 'casual_chat_correct' in session:
                    session['casual_chat_correct'] = 0
                if 'casual_chat_total' in session:
                    session['casual_chat_total'] = 0

                # Clear Claude client marker from session
                if 'claude_client' in session:
                    session.pop('claude_client', None)
                
                # Clear all claude clients from app context (they'll be recreated as needed)
                if hasattr(self.app, 'claude_clients'):
                    self.app.claude_clients = {}
                
                session.modified = True
                return jsonify({'status': 'success', 'message': 'Conversation cleared'})
                
            except Exception as e:
                print(f"Error clearing conversation: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/casual-chat/tts', methods=['POST'])
        @login_required
        def casual_chat_tts():
            """Text-to-speech endpoint for casual chat using Minimax."""
            try:
                from minimax_client import minimax_client
                
                # Parse request data
                data = request.get_json()
                
                if not data or 'text' not in data:
                    return jsonify({'error': 'Text is required'}), 400
                
                text = data.get('text', '').strip()
                if not text:
                    return jsonify({'error': 'Text cannot be empty'}), 400
                
                # Extract optional parameters
                character = data.get('character')  # 'harry' or 'sally'
                voice_id = data.get('voice_id')
                speed = data.get('speed')
                volume = data.get('vol')
                pitch = data.get('pitch')
                
                print(f"[TTS REQUEST] Character: {character}, Text length: {len(text)}")
                
                # Use Minimax client to synthesize speech
                success, result = minimax_client.synthesize_speech(
                    text=text,
                    character=character,
                    voice_id=voice_id,
                    speed=speed,
                    volume=volume,
                    pitch=pitch
                )
                
                if success:
                    # Return the result dict directly (matching GTA-V2)
                    return jsonify(result)
                else:
                    # Return error
                    return jsonify(result), 500
                    
            except Exception as e:
                print(f"Error in TTS endpoint: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/user-progress', methods=['GET'])
        @login_required
        def get_user_progress():
            """Get current user's progress for the active language pair."""
            try:
                from progress.progress_manager import ProgressManager
                from progress.exercise_progress_manager import ExerciseProgressManager
                from topics.topic_manager import TopicManager
                from tests.test_manager import TestManager

                user_id = session.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User not authenticated'}), 401

                # Get language pair from query params or session
                input_lang = request.args.get('input_language')
                target_lang = request.args.get('target_language')

                # Initialize managers
                progress_manager = ProgressManager()
                exercise_manager = ExerciseProgressManager()
                topic_manager = TopicManager()
                test_manager = TestManager()

                # Get user progress
                user_progress = progress_manager.get_user_progress(
                    user_id, input_lang, target_lang
                )

                if not user_progress:
                    return jsonify({'error': 'No progress found for this language pair'}), 404

                # Get all topics for the level
                topics = topic_manager.get_all_topics_for_level(user_progress.current_level)

                # Get all topic progress to determine max accessible topic
                all_topic_progress = topic_manager.get_user_topic_progress(user_progress.id)

                # Get topic progress for each topic
                topic_progress_list = []
                completed_topics = []

                # Calculate the highest accessible topic
                # (highest completed topic + 1, or current topic if nothing completed)
                completed_topics_nums = [tp.topic_number for tp in all_topic_progress if tp.completed]
                max_accessible_topic = max(completed_topics_nums) + 1 if completed_topics_nums else user_progress.current_topic

                for topic in topics:
                    # Get topic completion status
                    topic_progress = next((tp for tp in all_topic_progress if tp.topic_number == topic.topic_number), None)

                    # Get exercise status for this topic
                    exercise_status = exercise_manager.get_topic_exercises_status(
                        user_progress.id, topic.topic_number
                    )

                    is_completed = topic_progress.completed if topic_progress else False
                    is_current = (topic.topic_number == user_progress.current_topic)
                    # A topic is locked if it's beyond the max accessible topic
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

                # Get test progress
                test_progress_list = []
                test_configs = [
                    {'type': 'checkpoint_1', 'after_topic': 3, 'number': 1},
                    {'type': 'checkpoint_2', 'after_topic': 6, 'number': 2},
                    {'type': 'checkpoint_3', 'after_topic': 9, 'number': 3},
                    {'type': 'final', 'after_topic': 12, 'number': 4}
                ]

                for test_config in test_configs:
                    test_progress = test_manager.get_test_progress(
                        user_progress.id, test_config['type']
                    )

                    # Check if test is unlocked (topics before it are complete)
                    required_topics = list(range(
                        test_config['after_topic'] - 2,
                        test_config['after_topic'] + 1
                    ))
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

                # Calculate overall progress (topics + tests)
                total_points = 16  # 12 topics + 4 tests
                completed_points = len(completed_topics)

                # Add passed tests to completed points
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

        @self.app.route('/api/check-completion-popup', methods=['GET'])
        @login_required
        def check_completion_popup():
            """Check if a completion popup should be shown for the current topic."""
            try:
                from topics.topic_manager import TopicManager

                user_id = session.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User not authenticated'}), 401

                # Get language pair from query params
                input_lang = request.args.get('input_language')
                target_lang = request.args.get('target_language')

                if not input_lang or not target_lang:
                    return jsonify({'show_popup': False}), 200

                # Get user progress ID
                progress_mgr = ProgressManager()
                user_progress = progress_mgr.get_or_create_progress(user_id, input_lang, target_lang)

                if not user_progress:
                    return jsonify({'show_popup': False}), 200

                # Check if popup is needed
                topic_mgr = TopicManager()
                popup_info = topic_mgr.check_completion_popup_needed(user_progress.id)

                if popup_info:
                    return jsonify(popup_info), 200
                else:
                    return jsonify({'show_popup': False}), 200

            except Exception as e:
                print(f"[ERROR] Checking completion popup: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/mark-popup-seen', methods=['POST'])
        @login_required
        def mark_popup_seen():
            """Mark that the completion popup has been shown for a topic."""
            try:
                from topics.topic_manager import TopicManager

                user_id = session.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User not authenticated'}), 401

                # Get data from request
                data = request.get_json()
                topic_number = data.get('topic_number')
                input_lang = data.get('input_language')
                target_lang = data.get('target_language')

                if not all([topic_number, input_lang, target_lang]):
                    return jsonify({'error': 'Missing required fields'}), 400

                # Get user progress ID
                progress_mgr = ProgressManager()
                user_progress = progress_mgr.get_or_create_progress(user_id, input_lang, target_lang)

                if not user_progress:
                    return jsonify({'error': 'User progress not found'}), 404

                # Mark popup as seen
                topic_mgr = TopicManager()
                success, message = topic_mgr.mark_popup_seen(user_progress.id, topic_number)

                if success:
                    return jsonify({'success': True, 'message': message}), 200
                else:
                    return jsonify({'error': message}), 400

            except Exception as e:
                print(f"[ERROR] Marking popup seen: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/navigate-to-topic', methods=['POST'])
        @login_required
        def navigate_to_topic():
            """Navigate to a different topic."""
            try:
                from topics.topic_manager import TopicManager

                user_id = session.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User not authenticated'}), 401

                # Get data from request
                data = request.get_json()
                new_topic = data.get('topic_number')
                input_lang = data.get('input_language')
                target_lang = data.get('target_language')

                if not all([new_topic, input_lang, target_lang]):
                    return jsonify({'error': 'Missing required fields'}), 400

                # Get user progress ID
                progress_mgr = ProgressManager()
                user_progress = progress_mgr.get_or_create_progress(user_id, input_lang, target_lang)

                if not user_progress:
                    return jsonify({'error': 'User progress not found'}), 404

                # Navigate to the new topic
                topic_mgr = TopicManager()
                success, result = topic_mgr.navigate_to_topic(user_progress.id, new_topic)

                if success:
                    return jsonify({'success': True, **result}), 200
                else:
                    return jsonify({'error': result.get('error', 'Navigation failed')}), 400

            except Exception as e:
                print(f"[ERROR] Navigating to topic: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/casual-chat/scenario', methods=['GET'])
        @login_required
        def get_chat_scenario():
            """Get dynamic scenario for current user's topic and language pair."""
            try:
                from scenarios.scenario_manager import ScenarioManager

                user_id = session.get('user_id')
                if not user_id:
                    return jsonify({'error': 'User not authenticated'}), 401

                # Get character from query params (default to harry)
                character = request.args.get('character', 'harry')

                # Get topic override from session if available
                topic_override = session.get('exercise_topic')
                if topic_override:
                    print(f"[INFO] Scenario - Using topic override from session: {topic_override}")

                # Initialize scenario manager
                scenario_manager = ScenarioManager()

                # Get scenario for user
                scenario_text, context = scenario_manager.get_scenario_for_user(user_id, character, topic_override)

                # Return scenario and context
                return jsonify({
                    'scenario': scenario_text,
                    'context': context,
                    'status': 'success'
                })

            except Exception as e:
                print(f"Error fetching scenario: {e}")
                return jsonify({'error': str(e)}), 500

        # Email Writing Exercise Routes
        @self.app.route('/writing-practice')
        @login_required
        def email_writing():
            """Email writing exercise page."""
            try:
                # Get user's language context
                user_id = session.get('user_id')

                # Get topic override from URL parameter if provided
                topic_override = request.args.get('topic', type=int)
                if topic_override:
                    # Store in session for API endpoints to use
                    session['exercise_topic'] = topic_override

                # Get user's current language progress
                progress_mgr = ProgressManager()
                user_progress = progress_mgr.get_user_progress(user_id) if user_id else None

                # Check if user has selected languages
                if not user_progress:
                    flash('Please select your languages first.', 'info')
                    return redirect(url_for('dashboard'))

                # Prepare context for template
                context = {
                    'input_language': user_progress.input_language,
                    'target_language': user_progress.target_language,
                    'current_level': user_progress.current_level
                }

                return render_template('writing_email.html', **context)
            except Exception as e:
                print(f"Error loading email writing page: {e}")
                flash('Error loading writing exercise.', 'error')
                return redirect(url_for('exercises'))

        @self.app.route('/api/writing-practice/generate', methods=['POST'])
        @login_required
        def generate_email_letter():
            """Generate a letter for the email writing exercise."""
            try:
                import uuid
                from email_writing.exercise_manager import EmailExerciseManager

                # Get current user
                user_id = session.get('user_id')

                # Get topic override from session if available
                topic_override = session.get('exercise_topic')
                print(f"[INFO] Email Writing - Using topic override from session: {topic_override}")

                # Prepare user context - pass the user_id and optional topic override
                # The EmailExerciseManager will fetch the full context
                user_context = {
                    'user_id': user_id,
                    'topic_override': topic_override
                }

                # Get or create session ID
                session_id = session.get('email_session_id')
                if not session_id:
                    session_id = str(uuid.uuid4())
                    session['email_session_id'] = session_id

                # Get or create exercise session data
                exercise_session_key = f'email_writing_{session_id}'
                if exercise_session_key not in session:
                    session[exercise_session_key] = {}
                session_data = session[exercise_session_key]

                # Initialize exercise manager - no YAML needed anymore
                exercise_manager = EmailExerciseManager()

                # Process the request
                success, result = exercise_manager.process_exercise_request(
                    action='generate',
                    data={},
                    user_context=user_context,
                    session_data=session_data
                )

                # Update session data
                session[exercise_session_key] = session_data
                session.modified = True

                if success:
                    return jsonify(result)
                else:
                    return jsonify(result), 500

            except Exception as e:
                print(f"[ERROR] Error generating letter: {e}")
                import traceback
                print(traceback.format_exc())
                return jsonify({'error': f'Failed to generate letter: {str(e)}'}), 500

        @self.app.route('/api/writing-practice/submit', methods=['POST'])
        @login_required
        def submit_email_response():
            """Submit and evaluate a response for the email writing exercise."""
            try:
                from email_writing.exercise_manager import EmailExerciseManager

                # Get current user
                user_id = session.get('user_id')

                # Prepare user context
                user_context = {
                    'user_id': user_id,
                    'level': 'intermediate'
                }

                # Get session ID
                session_id = session.get('email_session_id', 'default')

                # Get exercise session data
                exercise_session_key = f'email_writing_{session_id}'
                session_data = session.get(exercise_session_key, {})

                # Get request data
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400

                # Initialize exercise manager - no YAML needed anymore
                exercise_manager = EmailExerciseManager()

                # Process the request
                success, result = exercise_manager.process_exercise_request(
                    action='evaluate',
                    data=data,
                    user_context=user_context,
                    session_data=session_data
                )

                # Update session data
                session[exercise_session_key] = session_data
                session.modified = True

                if success:
                    # Save score if this was a comprehensive feedback (second attempt)
                    if result.get('feedback_type') == 'comprehensive' and 'score' in result:
                        try:
                            from progress.exercise_progress_manager import ExerciseProgressManager
                            from progress.progress_manager import ProgressManager

                            # Get user's progress record
                            progress_manager = ProgressManager()

                            # Get language pair from session data (stored by exercise_manager)
                            input_lang = session_data.get('input_language', 'english')
                            target_lang = session_data.get('target_language', 'german')

                            # Get user progress ID
                            user_progress = progress_manager.get_user_progress(
                                user_id, input_lang, target_lang
                            )

                            if user_progress:
                                # Record the exercise attempt
                                exercise_manager_db = ExerciseProgressManager()
                                db_result = exercise_manager_db.record_exercise_attempt(
                                    user_progress_id=user_progress.id,
                                    topic_number=user_progress.current_topic,
                                    exercise_type='email_writing',
                                    score=result['score']
                                )

                                # Add progress info to response
                                result['exercise_completed'] = db_result.get('newly_completed', False)
                                result['topic_advanced'] = db_result.get('topic_advanced', False)

                                print(f"[SCORE SAVED] Email Writing: {result['score']}%")
                        except Exception as e:
                            print(f"[ERROR] Saving email writing score: {e}")

                    return jsonify(result)
                else:
                    return jsonify(result), 500

            except Exception as e:
                print(f"[ERROR] Error evaluating response: {e}")
                import traceback
                print(traceback.format_exc())
                return jsonify({'error': f'Failed to evaluate response: {str(e)}'}), 500