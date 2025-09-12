from database import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

class LevelRule(db.Model):
    """Model for storing level-specific rules and guidelines"""
    __tablename__ = 'level_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False, unique=True)  # A1, A2, B1, B2
    base_word_limit = db.Column(db.Integer, nullable=False)  # Default word limit for this level
    grammar_rules = db.Column(JSON, nullable=False)  # Allowed tenses, structures
    vocabulary_complexity = db.Column(db.String(50), nullable=False)  # basic, intermediate, advanced
    general_guidelines = db.Column(db.Text, nullable=False)  # Level-specific guidelines
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, level, base_word_limit, grammar_rules, vocabulary_complexity, general_guidelines):
        """Initialize level rule"""
        self.level = level.upper()
        self.base_word_limit = base_word_limit
        self.grammar_rules = grammar_rules
        self.vocabulary_complexity = vocabulary_complexity
        self.general_guidelines = general_guidelines
    
    def to_dict(self):
        """Convert level rule to dictionary"""
        return {
            'id': self.id,
            'level': self.level,
            'base_word_limit': self.base_word_limit,
            'grammar_rules': self.grammar_rules,
            'vocabulary_complexity': self.vocabulary_complexity,
            'general_guidelines': self.general_guidelines,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<LevelRule {self.level}: {self.base_word_limit} words>'