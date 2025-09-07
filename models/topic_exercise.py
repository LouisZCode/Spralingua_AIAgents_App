from database import db
from sqlalchemy.dialects.postgresql import JSON

class TopicExercise(db.Model):
    """Model for storing specific exercises within topics"""
    __tablename__ = 'topic_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    topic_definition_id = db.Column(db.Integer, db.ForeignKey('topic_definitions.id', ondelete='CASCADE'), nullable=False)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_types.id', ondelete='CASCADE'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)  # Order within topic
    specific_prompt = db.Column(db.Text)  # Override/addition to base prompt
    context_data = db.Column(JSON)  # Extra data like letter content, audio file, etc.
    difficulty_modifier = db.Column(db.String(20), default='normal')  # easy, normal, challenge
    
    # Unique constraint for topic + exercise number
    __table_args__ = (
        db.UniqueConstraint('topic_definition_id', 'exercise_number', name='_topic_exercise_uc'),
    )
    
    def __init__(self, topic_definition_id, exercise_type_id, exercise_number, 
                 specific_prompt=None, context_data=None, difficulty_modifier='normal'):
        """Initialize topic exercise"""
        self.topic_definition_id = topic_definition_id
        self.exercise_type_id = exercise_type_id
        self.exercise_number = exercise_number
        self.specific_prompt = specific_prompt
        self.context_data = context_data or {}
        self.difficulty_modifier = difficulty_modifier
    
    def get_combined_prompt(self):
        """Get the combined prompt from base type and specific override"""
        base_prompt = self.exercise_type.base_prompt_template if self.exercise_type else ""
        topic_prompt = self.topic.llm_prompt_template if self.topic else ""
        
        # Combine prompts intelligently
        combined = f"{base_prompt}\n\nTopic Context: {topic_prompt}"
        if self.specific_prompt:
            combined += f"\n\nSpecific Instructions: {self.specific_prompt}"
        
        return combined
    
    def to_dict(self):
        """Convert topic exercise to dictionary"""
        return {
            'id': self.id,
            'topic_definition_id': self.topic_definition_id,
            'exercise_type_id': self.exercise_type_id,
            'exercise_number': self.exercise_number,
            'specific_prompt': self.specific_prompt,
            'context_data': self.context_data,
            'difficulty_modifier': self.difficulty_modifier,
            'combined_prompt': self.get_combined_prompt()
        }
    
    def __repr__(self):
        return f'<TopicExercise Topic{self.topic_definition_id}-Ex{self.exercise_number}>'