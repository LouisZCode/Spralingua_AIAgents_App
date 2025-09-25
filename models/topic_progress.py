from datetime import datetime
from database import db

class TopicProgress(db.Model):
    """Model for tracking user progress through topics"""
    __tablename__ = 'topic_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_progress_id = db.Column(db.Integer, db.ForeignKey('user_progress.id', ondelete='CASCADE'), nullable=False)
    level = db.Column(db.String(10), nullable=False)  # A1, A2, B1, B2
    topic_number = db.Column(db.Integer, nullable=False)  # 1-16
    completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime)
    exercises_completed = db.Column(db.Integer, default=0, nullable=False)
    total_exercises = db.Column(db.Integer, nullable=False)  # Total exercises in this topic
    has_seen_completion_popup = db.Column(db.Boolean, default=False, nullable=False)  # Track if user saw completion popup

    # Relationship to UserProgress
    user_progress = db.relationship('UserProgress', backref=db.backref('topic_records', lazy='dynamic', cascade='all, delete-orphan'))

    # Unique constraint for user progress + level + topic number
    __table_args__ = (
        db.UniqueConstraint('user_progress_id', 'level', 'topic_number', name='_user_level_topic_uc'),
    )
    
    def __init__(self, user_progress_id, level, topic_number, total_exercises):
        """Initialize topic progress"""
        self.user_progress_id = user_progress_id
        self.level = level.upper()  # Ensure uppercase (A1, A2, B1, B2)
        self.topic_number = topic_number
        self.total_exercises = total_exercises
        self.exercises_completed = 0
        self.completed = False
    
    def complete_exercise(self):
        """Mark an exercise as completed"""
        self.exercises_completed = min(self.exercises_completed + 1, self.total_exercises)
        
        # Check if topic is fully completed
        if self.exercises_completed >= self.total_exercises:
            self.completed = True
            self.completed_at = datetime.utcnow()
        
        return self.completed
    
    def mark_complete(self):
        """Mark this topic as complete"""
        self.completed = True
        self.completed_at = datetime.utcnow()

    def reset_progress(self):
        """Reset progress for this topic"""
        self.exercises_completed = 0
        self.completed = False
        self.completed_at = None
        self.has_seen_completion_popup = False

    def mark_popup_seen(self):
        """Mark that the completion popup has been shown for this topic"""
        self.has_seen_completion_popup = True
    
    def get_progress_percentage(self):
        """Get completion percentage for this topic"""
        if self.total_exercises == 0:
            return 0
        return int((self.exercises_completed / self.total_exercises) * 100)
    
    def to_dict(self):
        """Convert topic progress to dictionary"""
        return {
            'id': self.id,
            'user_progress_id': self.user_progress_id,
            'level': self.level,
            'topic_number': self.topic_number,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'exercises_completed': self.exercises_completed,
            'total_exercises': self.total_exercises,
            'progress_percentage': self.get_progress_percentage(),
            'has_seen_completion_popup': self.has_seen_completion_popup
        }

    def __repr__(self):
        status = "[COMPLETED]" if self.completed else f"{self.exercises_completed}/{self.total_exercises}"
        return f'<TopicProgress {self.level}-Topic{self.topic_number} {status}>'