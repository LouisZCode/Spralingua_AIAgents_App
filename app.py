from flask import Flask, render_template, session, redirect, url_for
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

# Initialize authentication
from auth import AuthManager
from auth.auth_routes import AuthRoutes

auth_manager = AuthManager()
auth_routes = AuthRoutes(app, auth_manager)

@app.route('/')
def landing():
    """Landing page route"""
    # If user is logged in, redirect to dashboard
    if session.get('authenticated'):
        return redirect(url_for('dashboard'))
    
    # Add timestamp for cache busting
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return render_template('landing.html', timestamp=timestamp)

# Context processor to make timestamp available to all templates
@app.context_processor
def inject_timestamp():
    return {'timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S')}

if __name__ == '__main__':
    app.run(debug=True, port=5000)