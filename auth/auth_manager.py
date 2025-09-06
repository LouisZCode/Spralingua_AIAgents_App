# Simplified Authentication Manager for Spralingua

import re
from datetime import datetime
from typing import Optional, Dict, Tuple, Any
from flask import current_app
from flask_bcrypt import Bcrypt

class AuthManager:
    """Manages user authentication, registration, and session handling."""
    
    def __init__(self):
        """Initialize authentication manager."""
        self._initialized = False
        self.bcrypt = None
    
    def _ensure_initialized(self):
        """Ensure authentication manager is initialized with Flask context."""
        if not self._initialized:
            if not current_app:
                raise RuntimeError("AuthManager requires Flask application context")
            self.bcrypt = Bcrypt(current_app)
            self._initialized = True
    
    def register_user(self, email: str, password: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Register a new user with the platform.
        
        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            
        Returns:
            Tuple of (success, result_dict)
        """
        self._ensure_initialized()
        
        # Import here to avoid circular imports
        from models.user import User
        from database import db
        
        # Validate inputs
        is_valid, error_msg = self._validate_registration(email, password)
        if not is_valid:
            return False, {'error': error_msg}
        
        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email.lower()).first()
            
            if existing_user:
                return False, {'error': 'Email already registered'}
            
            # Create new user
            user = User(
                email=email.lower(),
                password=password,  # User model handles hashing
                progress_level=0
            )
            
            db.session.add(user)
            db.session.commit()
            
            print(f"[AUTH] User registered successfully: {email}")
            
            return True, {
                'user': user,
                'user_id': user.id,
                'email': user.email,
                'message': 'Registration successful'
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Registration failed: {str(e)}"
            print(f"[AUTH ERROR] {error_msg}")
            return False, {'error': error_msg}
    
    def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[Any]]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            Tuple of (success, user_object)
        """
        self._ensure_initialized()
        
        # Import here to avoid circular imports
        from models.user import User
        
        try:
            # Find user by email
            user = User.query.filter_by(email=email.lower()).first()
            
            if not user:
                print(f"[AUTH WARNING] User not found: {email}")
                return False, None
            
            # Check password
            if not user.check_password(password):
                print(f"[AUTH WARNING] Invalid password for user: {email}")
                return False, None
            
            # Update last login
            user.updated_at = datetime.utcnow()
            from database import db
            db.session.commit()
            
            print(f"[AUTH] User authenticated: {email}")
            return True, user
            
        except Exception as e:
            print(f"[AUTH ERROR] Authentication error: {str(e)}")
            return False, None
    
    def login_user(self, user: Any, session: Dict) -> None:
        """
        Log in a user by setting session data.
        
        Args:
            user: User object
            session: Flask session dict
        """
        session['user_id'] = user.id
        session['email'] = user.email
        session['authenticated'] = True
        session['login_time'] = datetime.utcnow().isoformat()
        session['progress_level'] = user.progress_level
        
        print(f"[AUTH] User logged in: {user.email}")
    
    def logout_user(self, session: Dict) -> None:
        """
        Log out a user by clearing session data.
        
        Args:
            session: Flask session dict
        """
        email = session.get('email', 'Unknown')
        
        # Clear authentication-related session data
        session.pop('user_id', None)
        session.pop('email', None)
        session.pop('authenticated', None)
        session.pop('login_time', None)
        session.pop('progress_level', None)
        
        print(f"[AUTH] User logged out: {email}")
    
    def _validate_registration(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate registration inputs.
        
        Args:
            email: Email address
            password: Password
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, 'Invalid email format'
        
        # Validate email length
        if len(email) > 120:
            return False, 'Email too long (max 120 characters)'
        
        # Validate password length
        if len(password) < 8:
            return False, 'Password must be at least 8 characters long'
        
        if len(password) > 128:
            return False, 'Password too long (max 128 characters)'
        
        return True, None
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        self._ensure_initialized()
        return self.bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Plain text password
            password_hash: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        self._ensure_initialized()
        return self.bcrypt.check_password_hash(password_hash, password)