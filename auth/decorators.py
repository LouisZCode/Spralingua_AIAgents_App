# Authentication Decorators

from functools import wraps
from flask import session, redirect, url_for, request, jsonify

def login_required(f):
    """
    Decorator to require authentication for a route.
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return 'This route requires login'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated') or not session.get('user_id'):
            # For API endpoints, return JSON error
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            
            # For regular routes, redirect to login
            # Store the URL to redirect back after login
            session['next_url'] = request.url
            return redirect(url_for('auth_login'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def guest_only(f):
    """
    Decorator to ensure route is only accessible to non-authenticated users.
    Useful for login/register pages.
    
    Usage:
        @app.route('/login')
        @guest_only
        def login():
            return 'Login page'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is actually authenticated
        is_authenticated = session.get('authenticated', False) and session.get('user_id') is not None
        
        if is_authenticated:
            # Redirect authenticated users to dashboard
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    
    return decorated_function