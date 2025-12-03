"""
Spralingua - AI-powered language learning platform.
Main application entry point.
"""

from flask import Flask, session, request, jsonify
from datetime import datetime

from config import Config
from database import db, bcrypt
from routes import register_blueprints
from progress.progress_manager import ProgressManager


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)
    Config.log_config()

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Import models (required for SQLAlchemy relationships)
    from models.user import User
    from models.user_progress import UserProgress
    from models.topic_definition import TopicDefinition
    from models.exercise_type import ExerciseType
    from models.topic_exercise import TopicExercise
    from models.topic_progress import TopicProgress
    from models.test_progress import TestProgress
    from models.level_rule import LevelRule
    from models.exercise_progress import ExerciseProgress

    # Register blueprints
    register_blueprints(app)

    # Register additional routes
    register_progress_routes(app)

    # Register context processors
    register_context_processors(app)

    return app


def register_progress_routes(app):
    """Register progress-related routes that aren't in blueprints."""
    progress_manager = ProgressManager()

    @app.route('/api/save-progress', methods=['POST'])
    def save_progress():
        """API endpoint to save user's language selection progress."""
        if not session.get('authenticated'):
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401

        try:
            data = request.get_json()

            required = ('input_language', 'target_language', 'current_level')
            if not all(k in data for k in required):
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400

            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'success': False, 'error': 'User ID not found in session'}), 400

            success, result = progress_manager.save_progress_with_initialization(
                user_id=user_id,
                input_language=data['input_language'],
                target_language=data['target_language'],
                current_level=data['current_level']
            )

            if success:
                return jsonify({'success': True, 'data': result}), 200
            else:
                return jsonify({'success': False, 'error': result.get('error', 'Failed to save progress')}), 500

        except Exception as e:
            print(f"[ERROR] save_progress API: {e}")
            return jsonify({'success': False, 'error': 'Internal server error'}), 500


def register_context_processors(app):
    """Register Jinja2 context processors."""

    @app.context_processor
    def inject_timestamp():
        return {'timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S')}


# Create app instance
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
