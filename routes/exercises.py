"""
Exercise routes blueprint.
Handles exercise pages: exercises hub, casual chat, writing practice.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from auth.decorators import login_required
from progress.progress_manager import ProgressManager
from language.language_mapper import LanguageMapper


exercises_bp = Blueprint('exercises', __name__)


@exercises_bp.route('/exercises')
@login_required
def exercises():
    """Exercises page for practicing languages."""
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


@exercises_bp.route('/casual-chat')
@login_required
def casual_chat():
    """Casual chat conversation practice page."""
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
        return redirect(url_for('auth.dashboard'))

    # Map target language to speech recognition code
    target_language = user_progress.target_language
    speech_code = LanguageMapper.get_speech_code(target_language)

    # If somehow the language isn't supported, redirect
    if not speech_code:
        flash('Language configuration error. Please select your languages again.', 'error')
        return redirect(url_for('auth.dashboard'))

    return render_template('casual_chat.html',
                           email=email,
                           target_language=target_language,
                           speech_code=speech_code)


@exercises_bp.route('/writing-practice')
@login_required
def writing_practice():
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
            return redirect(url_for('auth.dashboard'))

        # Prepare context for template
        context = {
            'input_language': user_progress.input_language,
            'target_language': user_progress.target_language,
            'current_level': user_progress.current_level
        }

        return render_template('writing_email.html', **context)

    except Exception as e:
        print(f"[ERROR] Loading email writing page: {e}")
        flash('Error loading writing exercise.', 'error')
        return redirect(url_for('exercises.exercises'))
