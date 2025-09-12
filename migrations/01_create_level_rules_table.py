"""
Migration script to create and populate level_rules table
This stores level-specific configuration extracted from conversation_template.yaml
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app

# Import the model
from models.level_rule import LevelRule

def create_and_populate_level_rules():
    """Create level_rules table and populate with initial data"""
    
    # Define level rules data (extracted from conversation_template.yaml)
    level_rules_data = [
        {
            'level': 'A1',
            'base_word_limit': 40,
            'vocabulary_complexity': 'basic',
            'grammar_rules': {
                'tenses': ['present_simple'],
                'structures': ['basic_questions', 'simple_statements'],
                'avoid': ['complex_clauses', 'perfect_tenses', 'conditionals']
            },
            'general_guidelines': """- Use present simple tense primarily
- Basic vocabulary only (high-frequency words)
- Short, simple sentences
- One idea per sentence
- Avoid complex grammar structures
- Use basic question forms"""
        },
        {
            'level': 'A2',
            'base_word_limit': 50,
            'vocabulary_complexity': 'elementary',
            'grammar_rules': {
                'tenses': ['present_simple', 'past_simple', 'basic_future'],
                'structures': ['simple_connectors', 'basic_modals', 'simple_subordinate_clauses'],
                'avoid': ['perfect_tenses', 'complex_conditionals']
            },
            'general_guidelines': """- Use present, past simple, and basic future
- Common vocabulary and expressions
- Simple connecting words (and, but, because)
- Can use basic modal verbs
- Simple subordinate clauses
- Basic comparative forms"""
        },
        {
            'level': 'B1',
            'base_word_limit': 60,
            'vocabulary_complexity': 'intermediate',
            'grammar_rules': {
                'tenses': ['all_basic_tenses', 'present_perfect', 'past_continuous'],
                'structures': ['complex_sentences', 'first_second_conditionals', 'phrasal_verbs'],
                'avoid': ['very_formal_structures']
            },
            'general_guidelines': """- Use various tenses including perfect forms
- Broader vocabulary range
- Complex sentences with multiple clauses
- Conditional sentences (first and second)
- Phrasal verbs and idioms
- Express opinions and preferences clearly"""
        },
        {
            'level': 'B2',
            'base_word_limit': 70,
            'vocabulary_complexity': 'upper_intermediate',
            'grammar_rules': {
                'tenses': ['all_tenses'],
                'structures': ['all_structures', 'complex_argumentation', 'subtle_expressions'],
                'avoid': []
            },
            'general_guidelines': """- All tenses and complex grammar structures
- Rich vocabulary including abstract concepts
- Natural use of idioms and colloquialisms
- Complex argumentation and reasoning
- Subtle expressions of emotion and opinion
- Cultural references and humor"""
        }
    ]
    
    with app.app_context():
        try:
            # Create the table
            db.create_all()
            
            # Check if level rules already exist
            existing = LevelRule.query.count()
            if existing > 0:
                print(f"[WARNING] {existing} level rules already exist. Skipping population.")
                return False
            
            # Add all level rules
            for rule_data in level_rules_data:
                rule = LevelRule(
                    level=rule_data['level'],
                    base_word_limit=rule_data['base_word_limit'],
                    grammar_rules=rule_data['grammar_rules'],
                    vocabulary_complexity=rule_data['vocabulary_complexity'],
                    general_guidelines=rule_data['general_guidelines']
                )
                db.session.add(rule)
                print(f"[OK] Added level rule for {rule_data['level']}")
            
            # Commit all changes
            db.session.commit()
            print(f"\n[SUCCESS] Successfully created and populated level_rules table with {len(level_rules_data)} rules!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to create/populate level_rules: {e}")
            return False

if __name__ == '__main__':
    success = create_and_populate_level_rules()
    if not success:
        sys.exit(1)