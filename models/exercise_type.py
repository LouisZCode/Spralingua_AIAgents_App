from database import db

class ExerciseType(db.Model):
    """Model for storing different types of exercises"""
    __tablename__ = 'exercise_types'
    
    id = db.Column(db.Integer, primary_key=True)
    type_key = db.Column(db.String(50), unique=True, nullable=False)  # conversation, letter_response, etc.
    name = db.Column(db.String(100), nullable=False)  # Human-readable name
    base_prompt_template = db.Column(db.Text, nullable=False)  # Default LLM instructions for this type
    
    # Relationships
    exercises = db.relationship('TopicExercise', backref='exercise_type', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, type_key, name, base_prompt_template):
        """Initialize exercise type"""
        self.type_key = type_key.lower()
        self.name = name
        self.base_prompt_template = base_prompt_template
    
    def to_dict(self):
        """Convert exercise type to dictionary"""
        return {
            'id': self.id,
            'type_key': self.type_key,
            'name': self.name,
            'base_prompt_template': self.base_prompt_template
        }
    
    def __repr__(self):
        return f'<ExerciseType {self.type_key}: {self.name}>'