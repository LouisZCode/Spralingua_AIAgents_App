from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
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
        
        # Save progress using ProgressManager
        success, result = progress_manager.save_progress(
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

# Context processor to make timestamp available to all templates
@app.context_processor
def inject_timestamp():
    return {'timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S')}

if __name__ == '__main__':
    app.run(debug=True, port=5000)