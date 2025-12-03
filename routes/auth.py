"""
Authentication routes blueprint.
Handles login, register, logout, and dashboard.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from auth.forms import LoginForm, RegistrationForm
from auth.decorators import login_required, guest_only
from auth import AuthManager
from progress.progress_manager import ProgressManager


auth_bp = Blueprint('auth', __name__)

# Initialize managers
auth_manager = AuthManager()


@auth_bp.route('/login', methods=['GET', 'POST'])
@guest_only
def login():
    """Login page and handler."""
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        # Authenticate user
        success, user = auth_manager.authenticate_user(email, password)

        if success and user:
            # Log in the user
            auth_manager.login_user(user, session)

            # Set session as permanent if remember me is checked
            if remember_me:
                session.permanent = True

            # Redirect to next URL or dashboard
            next_url = session.pop('next_url', None)
            if next_url:
                return redirect(next_url)

            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
@guest_only
def register():
    """Registration page and handler."""
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        print(f"[REGISTRATION] Attempting to register user: {email}, name: {name}")

        # Register user with name
        success, result = auth_manager.register_user(email, name, password)

        if success:
            # Log the user in automatically
            user = result.get('user')
            auth_manager.login_user(user, session)

            print(f"[REGISTRATION] User registered successfully: {email}")
            flash(f'Registration successful! Welcome to Spralingua, {user.name}!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            error_msg = result.get('error', 'Registration failed')
            print(f"[REGISTRATION ERROR] {error_msg}")
            flash(error_msg, 'error')

    elif request.method == 'POST':
        # Form validation failed
        print(f"[REGISTRATION] Form validation errors: {form.errors}")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout handler."""
    auth_manager.logout_user(session)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('core.landing'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page for logged-in users."""
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
