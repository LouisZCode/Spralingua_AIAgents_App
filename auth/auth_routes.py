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
            email = session.get('email', 'User')
            return render_template('casual_chat.html', email=email)
        
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
                
                # Load the appropriate prompt file based on character
                if character == 'sally':
                    prompt_file = os.path.join('prompts', 'casual_chat_sally_prompts.yaml')
                else:
                    prompt_file = os.path.join('prompts', 'casual_chat_prompts.yaml')
                
                # Load prompts
                prompt_manager = PromptManager(prompt_file)
                system_prompt = prompt_manager.get_prompt('casual_chat_prompt', '')
                
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
                
                # Generate language hint for each message (except the last)
                if message_count < 6:
                    hint_data = generate_language_hint(message, prompt_manager, claude, 'intermediate')
                    response_data['hint'] = hint_data
                
                # Generate comprehensive feedback after 5 messages
                if message_count == 5:
                    feedback_data = generate_comprehensive_feedback(
                        session['casual_chat_messages'], 
                        prompt_manager,
                        claude, 
                        'intermediate'
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
                
                # Clear Claude client
                if hasattr(self.app, 'claude_clients'):
                    session_id = session.get('_id', id(session))
                    if session_id in self.app.claude_clients:
                        self.app.claude_clients[session_id].clear_conversation_history()
                
                session.modified = True
                return jsonify({'status': 'success', 'message': 'Conversation cleared'})
                
            except Exception as e:
                print(f"Error clearing conversation: {e}")
                return jsonify({'error': str(e)}), 500