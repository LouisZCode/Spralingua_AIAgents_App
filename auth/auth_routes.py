# Authentication Routes for Spralingua

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .auth_manager import AuthManager
from .decorators import login_required, guest_only

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
                email = form.email.data
                password = form.password.data
                
                # Register user
                success, result = self.auth_manager.register_user(email, password)
                
                if success:
                    # Log the user in automatically
                    user = result.get('user')
                    self.auth_manager.login_user(user, session)
                    
                    flash('Registration successful! Welcome to Spralingua!', 'success')
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
                        dynamic_prompt, context = prompt_builder.build_prompt(
                            session['user_id'], 
                            character
                        )
                        
                        if dynamic_prompt:
                            system_prompt = dynamic_prompt
                            user_context = context
                            print(f"[INFO] Using dynamic prompt for user {session['user_id']}")
                            print(f"[INFO] Context: {context.get('input_language')} -> {context.get('target_language')}, Level: {context.get('level')}, Topic: {context.get('topic_title')}")
                    except Exception as e:
                        print(f"[WARNING] Dynamic prompt failed, falling back: {e}")
                
                # Fallback to static prompts if dynamic system not available
                if not system_prompt:
                    # Load the appropriate prompt file based on character
                    if character == 'sally':
                        prompt_file = os.path.join('prompts', 'casual_chat_sally_prompts.yaml')
                    else:
                        prompt_file = os.path.join('prompts', 'casual_chat_prompts.yaml')
                    
                    # Load prompts
                    prompt_manager = PromptManager(prompt_file)
                    system_prompt = prompt_manager.get_prompt('casual_chat_prompt', '')
                    print(f"[INFO] Using static prompt for character: {character}")
                
                # Track message count in session
                if 'casual_chat_messages' not in session:
                    session['casual_chat_messages'] = []
                
                # Add current message to history
                session['casual_chat_messages'].append(message)
                message_count = len(session['casual_chat_messages'])
                
                # Send message to Claude with character prompt
                response = claude.send_message(message, system_prompt)
                
                # Prepare response data
                response_data = {
                    'response': response,
                    'message_count': message_count,
                    'total_messages_required': 6
                }
                
                # Determine the level for feedback (from context or default)
                feedback_level = user_context.get('level', 'A1').lower()
                # Map database levels to feedback levels
                level_map = {'a1': 'beginner', 'a2': 'elementary', 'b1': 'intermediate', 'b2': 'upper-intermediate'}
                feedback_level = level_map.get(feedback_level.lower(), 'intermediate')
                
                # Generate language hint for each message (except the last)
                if message_count < 6:
                    # Need to reload prompt_manager for feedback if using dynamic system
                    if USE_DYNAMIC_PROMPTS and 'user_id' in session and user_context:
                        # Use static prompt manager for feedback generation
                        if character == 'sally':
                            prompt_file = os.path.join('prompts', 'casual_chat_sally_prompts.yaml')
                        else:
                            prompt_file = os.path.join('prompts', 'casual_chat_prompts.yaml')
                        prompt_manager = PromptManager(prompt_file)
                    
                    hint_data = generate_language_hint(message, prompt_manager, claude, feedback_level)
                    response_data['hint'] = hint_data
                
                # Generate comprehensive feedback after 5 messages
                if message_count == 5:
                    # Need to reload prompt_manager for feedback if using dynamic system
                    if USE_DYNAMIC_PROMPTS and 'user_id' in session and user_context:
                        # Use static prompt manager for feedback generation
                        if character == 'sally':
                            prompt_file = os.path.join('prompts', 'casual_chat_sally_prompts.yaml')
                        else:
                            prompt_file = os.path.join('prompts', 'casual_chat_prompts.yaml')
                        prompt_manager = PromptManager(prompt_file)
                    
                    feedback_data = generate_comprehensive_feedback(
                        session['casual_chat_messages'], 
                        prompt_manager,
                        claude, 
                        feedback_level
                    )
                    response_data['comprehensive_feedback'] = feedback_data
                
                # Mark as complete after 6 messages
                if message_count >= 6:
                    response_data['module_completed'] = True
                    # Clear session for next conversation
                    session['casual_chat_messages'] = []
                
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

                # Initialize scenario manager
                scenario_manager = ScenarioManager()

                # Get scenario for user
                scenario_text, context = scenario_manager.get_scenario_for_user(user_id, character)

                # Return scenario and context
                return jsonify({
                    'scenario': scenario_text,
                    'context': context,
                    'status': 'success'
                })

            except Exception as e:
                print(f"Error fetching scenario: {e}")
                return jsonify({'error': str(e)}), 500