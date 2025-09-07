from datetime import datetime
from database import db

class TestProgress(db.Model):
    """Model for tracking user progress through tests"""
    __tablename__ = 'test_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_progress_id = db.Column(db.Integer, db.ForeignKey('user_progress.id', ondelete='CASCADE'), nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # checkpoint_1, checkpoint_2, final
    test_number = db.Column(db.Integer, nullable=False)  # 1, 2, or 3
    passed = db.Column(db.Boolean, default=False, nullable=False)
    score = db.Column(db.Integer)  # Percentage score (0-100)
    attempts = db.Column(db.Integer, default=0, nullable=False)
    passed_at = db.Column(db.DateTime)
    last_attempt_at = db.Column(db.DateTime)
    
    # Relationship to UserProgress
    user_progress = db.relationship('UserProgress', backref=db.backref('test_records', lazy='dynamic', cascade='all, delete-orphan'))
    
    # Unique constraint for user progress + test type
    __table_args__ = (
        db.UniqueConstraint('user_progress_id', 'test_type', name='_user_test_uc'),
    )
    
    def __init__(self, user_progress_id, test_type, test_number):
        """Initialize test progress"""
        self.user_progress_id = user_progress_id
        self.test_type = test_type
        self.test_number = test_number
        self.passed = False
        self.attempts = 0
    
    def record_attempt(self, score, passing_threshold=50):
        """Record a test attempt"""
        self.attempts += 1
        self.score = score
        self.last_attempt_at = datetime.utcnow()
        
        # Check if passed (default threshold is 50%)
        if score >= passing_threshold:
            self.passed = True
            self.passed_at = datetime.utcnow()
        
        return self.passed
    
    def reset_test(self):
        """Reset test progress"""
        self.passed = False
        self.score = None
        self.attempts = 0
        self.passed_at = None
        self.last_attempt_at = None
    
    def get_status(self):
        """Get test status"""
        if self.passed:
            return 'passed'
        elif self.attempts > 0:
            return 'failed'
        else:
            return 'not_attempted'
    
    def is_unlocked(self, completed_topics):
        """Check if test is unlocked based on completed topics"""
        required_topics = {
            'checkpoint_1': list(range(1, 5)),  # Topics 1-4
            'checkpoint_2': list(range(5, 9)),  # Topics 5-8
            'final': list(range(9, 13))  # Topics 9-12
        }
        
        if self.test_type in required_topics:
            return all(topic in completed_topics for topic in required_topics[self.test_type])
        return False
    
    def to_dict(self):
        """Convert test progress to dictionary"""
        return {
            'id': self.id,
            'user_progress_id': self.user_progress_id,
            'test_type': self.test_type,
            'test_number': self.test_number,
            'passed': self.passed,
            'score': self.score,
            'attempts': self.attempts,
            'passed_at': self.passed_at.isoformat() if self.passed_at else None,
            'last_attempt_at': self.last_attempt_at.isoformat() if self.last_attempt_at else None,
            'status': self.get_status()
        }
    
    def __repr__(self):
        status = "✓" if self.passed else f"({self.attempts} attempts)"
        return f'<TestProgress {self.test_type} {status}>'