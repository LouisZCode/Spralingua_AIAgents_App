from database import db
from sqlalchemy.dialects.postgresql import JSON

class TopicDefinition(db.Model):
    """Model for storing topic definitions across all levels"""
    __tablename__ = 'topic_definitions'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False)  # A1, A2, B1, B2
    topic_number = db.Column(db.Integer, nullable=False)  # 1-12
    title_key = db.Column(db.String(100), nullable=False)  # For translations
    subtopics = db.Column(JSON, nullable=False)  # List of subtopic strings
    conversation_contexts = db.Column(JSON, nullable=False)  # List of context scenarios
    llm_prompt_template = db.Column(db.Text, nullable=False)  # Natural language instructions for LLM
    
    # Relationships
    exercises = db.relationship('TopicExercise', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    
    # Unique constraint for level + topic number
    __table_args__ = (
        db.UniqueConstraint('level', 'topic_number', name='_level_topic_uc'),
    )
    
    def __init__(self, level, topic_number, title_key, subtopics, conversation_contexts, llm_prompt_template):
        """Initialize topic definition"""
        self.level = level.upper()
        self.topic_number = topic_number
        self.title_key = title_key
        self.subtopics = subtopics
        self.conversation_contexts = conversation_contexts
        self.llm_prompt_template = llm_prompt_template
    
    def to_dict(self):
        """Convert topic definition to dictionary"""
        return {
            'id': self.id,
            'level': self.level,
            'topic_number': self.topic_number,
            'title_key': self.title_key,
            'subtopics': self.subtopics,
            'conversation_contexts': self.conversation_contexts,
            'llm_prompt_template': self.llm_prompt_template
        }
    
    def __repr__(self):
        return f'<TopicDefinition {self.level}-Topic{self.topic_number}: {self.title_key}>'