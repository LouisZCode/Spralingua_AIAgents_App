from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(32).hex())

# Fix Railway's postgres:// to postgresql:// for SQLAlchemy
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Log database connection info (masked for security)
if database_url:
    masked_url = database_url[:50] + "..." + database_url[-20:] if len(database_url) > 70 else database_url[:50] + "..."
    print(f"[APP INIT] Connected to database: {masked_url}")
else:
    print("[APP INIT ERROR] No DATABASE_URL found!")

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
# Enable secure cookies in production (Railway sets RAILWAY_ENVIRONMENT)
app.config['SESSION_COOKIE_SECURE'] = bool(os.getenv('RAILWAY_ENVIRONMENT'))
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# WTForms configuration
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for CSRF tokens

# Initialize extensions from database module
from database import db, bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Import models after db initialization
from models.user import User
from models.user_progress import UserProgress
from models.topic_definition import TopicDefinition
from models.exercise_type import ExerciseType
from models.topic_exercise import TopicExercise
from models.topic_progress import TopicProgress
from models.test_progress import TestProgress
from models.level_rule import LevelRule
from models.exercise_progress import ExerciseProgress

# Initialize authentication
from auth import AuthManager
from auth.auth_routes import AuthRoutes

# Initialize progress manager
from progress.progress_manager import ProgressManager

auth_manager = AuthManager()
auth_routes = AuthRoutes(app, auth_manager)
progress_manager = ProgressManager()

@app.route('/')
def landing():
    """Landing page route"""
    # If user is logged in, redirect to dashboard
    if session.get('authenticated'):
        return redirect(url_for('dashboard'))
    
    # Add timestamp for cache busting
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return render_template('landing.html', timestamp=timestamp)

# API endpoint for saving progress
@app.route('/api/save-progress', methods=['POST'])
def save_progress():
    """API endpoint to save user's language selection progress"""
    # Check if user is logged in
    if not session.get('authenticated'):
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ('input_language', 'target_language', 'current_level')):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Get user ID from session
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID not found in session'}), 400
        
        # Save progress using ProgressManager with topic initialization
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
        print(f"Error in save_progress API: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Temporary endpoint for database initialization (remove after use)
@app.route('/init-db')
def init_database():
    """Initialize database tables and run migrations - ONE TIME USE ONLY"""
    try:
        results = []

        # Step 1: Create all tables
        results.append("[STEP 1] Creating all database tables...")
        db.create_all()
        results.append("[SUCCESS] All tables created via db.create_all()")

        # Step 2: Import and run migrations
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'migrations'))

        # Populate A1 topics
        results.append("[STEP 2] Populating A1 topics...")
        from populate_a1_topics import populate_a1_topics
        populate_a1_topics()
        results.append("[SUCCESS] A1 topics populated")

        # Populate exercise types
        results.append("[STEP 3] Populating exercise types...")
        from populate_exercise_types import populate_exercise_types
        populate_exercise_types()
        results.append("[SUCCESS] Exercise types populated")

        # Verify results
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        results.append(f"[VERIFY] Total tables: {len(tables)}")
        results.append(f"[VERIFY] Tables: {', '.join(sorted(tables))}")

        # Check data counts
        topic_count = db.session.execute(db.text('SELECT COUNT(*) FROM topic_definitions')).scalar()
        exercise_count = db.session.execute(db.text('SELECT COUNT(*) FROM exercise_types')).scalar()
        results.append(f"[DATA] Topics: {topic_count}, Exercise Types: {exercise_count}")

        return jsonify({
            'success': True,
            'message': 'Database initialized successfully!',
            'details': results
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Database initialization failed'
        }), 500

# Context processor to make timestamp available to all templates
@app.context_processor
def inject_timestamp():
    return {'timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S')}

if __name__ == '__main__':
    app.run(debug=True, port=5000)