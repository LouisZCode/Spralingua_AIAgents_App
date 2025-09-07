from datetime import datetime
from database import db

class UserProgress(db.Model):
    """Model for tracking user progress by language pair"""
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    input_language = db.Column(db.String(50), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    current_level = db.Column(db.String(10), nullable=False)
    progress_in_level = db.Column(db.Integer, default=0, nullable=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('progress_records', lazy='dynamic', cascade='all, delete-orphan'))
    
    # Unique constraint for user + language pair
    __table_args__ = (
        db.UniqueConstraint('user_id', 'input_language', 'target_language', name='_user_language_pair_uc'),
    )
    
    def __init__(self, user_id, input_language, target_language, current_level):
        """Initialize user progress record"""
        self.user_id = user_id
        self.input_language = input_language.lower()
        self.target_language = target_language.lower()
        self.current_level = current_level.upper()
        self.progress_in_level = 0
        self.last_accessed = datetime.utcnow()
    
    def update_progress(self, new_level=None, progress_in_level=None):
        """Update progress for this language pair"""
        if new_level:
            self.current_level = new_level.upper()
        if progress_in_level is not None:
            self.progress_in_level = progress_in_level
        self.last_accessed = datetime.utcnow()
    
    def to_dict(self):
        """Convert progress record to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'input_language': self.input_language,
            'target_language': self.target_language,
            'current_level': self.current_level,
            'progress_in_level': self.progress_in_level,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<UserProgress {self.input_language}→{self.target_language} @ {self.current_level}>'