# Authentication Routes for Spralingua

from flask import Flask, render_template, request, redirect, url_for, session, flash
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