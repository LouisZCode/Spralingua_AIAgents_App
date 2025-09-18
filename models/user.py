from datetime import datetime
from database import db, bcrypt

class User(db.Model):
    """Simplified User model with email, password, name, and progress tracking"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    progress_level = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, email, name, password, progress_level=0):
        """Initialize user with email, name, password, and optional progress level"""
        self.email = email.lower()  # Store email in lowercase
        self.name = name.strip()  # Store name with trimmed whitespace
        self.set_password(password)
        self.progress_level = progress_level
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches the stored hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def update_progress(self, new_level):
        """Update user's progress level"""
        self.progress_level = new_level
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<User {self.name} ({self.email}) - Level {self.progress_level}>'