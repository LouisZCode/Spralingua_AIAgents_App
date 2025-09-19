from datetime import datetime
from database import db

class ExerciseProgress(db.Model):
    """Model for tracking individual exercise completion within topics"""
    __tablename__ = 'exercise_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_progress_id = db.Column(db.Integer, db.ForeignKey('user_progress.id', ondelete='CASCADE'), nullable=False)
    topic_number = db.Column(db.Integer, nullable=False)  # 1-12
    exercise_type = db.Column(db.String(50), nullable=False)  # 'casual_chat', 'email_writing', etc.
    score = db.Column(db.Float, default=0.0, nullable=False)  # Percentage score (0-100)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    attempts = db.Column(db.Integer, default=0, nullable=False)
    best_score = db.Column(db.Float, default=0.0, nullable=False)  # Track best score achieved
    completed_at = db.Column(db.DateTime)
    last_attempt_at = db.Column(db.DateTime)

    # Additional tracking for Casual Chat
    messages_correct = db.Column(db.Integer, default=0)  # For casual chat tracking
    messages_total = db.Column(db.Integer, default=0)    # For casual chat tracking

    # Relationship to UserProgress
    user_progress = db.relationship('UserProgress', backref=db.backref('exercise_records', lazy='dynamic', cascade='all, delete-orphan'))

    # Unique constraint for user progress + topic + exercise type
    __table_args__ = (
        db.UniqueConstraint('user_progress_id', 'topic_number', 'exercise_type', name='_user_topic_exercise_uc'),
    )

    def __init__(self, user_progress_id, topic_number, exercise_type):
        """Initialize exercise progress"""
        self.user_progress_id = user_progress_id
        self.topic_number = topic_number
        self.exercise_type = exercise_type.lower()
        self.score = 0.0
        self.completed = False
        self.attempts = 0
        self.best_score = 0.0

    def record_attempt(self, score, messages_correct=None, messages_total=None):
        """
        Record an exercise attempt

        Args:
            score: The score achieved (0-100)
            messages_correct: Optional - for casual chat exercises
            messages_total: Optional - for casual chat exercises

        Returns:
            bool: True if exercise is now complete (score >= 50)
        """
        self.attempts += 1
        self.score = score
        self.last_attempt_at = datetime.utcnow()

        # Update best score
        if score > self.best_score:
            self.best_score = score

        # Update casual chat specific fields if provided
        if messages_correct is not None:
            self.messages_correct = messages_correct
        if messages_total is not None:
            self.messages_total = messages_total

        # Check if exercise is complete (50% threshold)
        if score >= 50 and not self.completed:
            self.completed = True
            self.completed_at = datetime.utcnow()

        return self.completed

    def reset_progress(self):
        """Reset progress for this exercise"""
        self.score = 0.0
        self.completed = False
        self.attempts = 0
        self.best_score = 0.0
        self.completed_at = None
        self.last_attempt_at = None
        self.messages_correct = 0
        self.messages_total = 0

    def get_completion_status(self):
        """Get completion status"""
        if self.completed:
            return 'completed'
        elif self.attempts > 0:
            return 'in_progress'
        else:
            return 'not_started'

    def to_dict(self):
        """Convert exercise progress to dictionary"""
        return {
            'id': self.id,
            'user_progress_id': self.user_progress_id,
            'topic_number': self.topic_number,
            'exercise_type': self.exercise_type,
            'score': self.score,
            'completed': self.completed,
            'attempts': self.attempts,
            'best_score': self.best_score,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_attempt_at': self.last_attempt_at.isoformat() if self.last_attempt_at else None,
            'messages_correct': self.messages_correct,
            'messages_total': self.messages_total,
            'status': self.get_completion_status()
        }

    def __repr__(self):
        status = "[OK]" if self.completed else f"({self.score:.0f}%)"
        return f'<ExerciseProgress T{self.topic_number}/{self.exercise_type} {status}>'