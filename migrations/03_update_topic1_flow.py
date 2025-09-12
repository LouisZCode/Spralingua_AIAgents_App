"""
Migration script to update A1 Topic 1 conversation flow
Adding "where exactly" question and increasing exchanges to 6
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from models.topic_definition import TopicDefinition

def update_topic1_flow():
    """Update A1 Topic 1 with enhanced conversation flow"""
    
    # Enhanced conversation flow with "where exactly" question
    enhanced_flow = [
        "Greeting + name introduction + ask their name",
        "Nice to meet you + ask where from (country)",
        "React to country + ask where exactly in that country",
        "React to specific location + say where you're from",
        "Ask how they are",
        "Share one simple hobby (snowboarding)"
    ]
    
    # Updated opening phrases to include the additional exchange
    updated_opening_phrases = {
        'german': "Hallo! Ich bin Harry. Wie heißt du?",
        'spanish': "¡Hola! Soy Harry. ¿Cómo te llamas?",
        'portuguese': "Olá! Eu sou o Harry. Como te chamas?",
        'english': "Hello! I'm Harry. What's your name?"
    }
    
    with app.app_context():
        try:
            # Find A1 Topic 1
            topic = TopicDefinition.query.filter_by(level='A1', topic_number=1).first()
            
            if not topic:
                print("[ERROR] A1 Topic 1 not found!")
                return False
            
            # Update conversation flow
            topic.conversation_flow = enhanced_flow
            
            # Update number of exchanges from 5 to 6
            topic.number_of_exchanges = 6
            
            # Keep the opening phrases (they're still good)
            if not topic.opening_phrases:
                topic.opening_phrases = updated_opening_phrases
            
            # Update the topic-specific rules to reflect 6 exchanges
            topic.topic_specific_rules = """STRICT RULES FOR A1 TOPIC 1:
- Maximum 15 words per response
- Use ONLY present simple tense
- NO complex sentences (no 'and' chains, no 'because', no 'that')
- Ask ONE question at a time
- Wait for response before next question
- When student says a country, ask "Where exactly in [country]?"
- Keep location questions simple and natural"""
            
            # Commit changes
            db.session.commit()
            
            print("[SUCCESS] Updated A1 Topic 1 conversation flow:")
            print("- Added 'where exactly' question as step 3")
            print("- Increased exchanges from 5 to 6")
            print("- Flow now includes:")
            for i, step in enumerate(enhanced_flow, 1):
                print(f"  {i}. {step}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to update Topic 1: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = update_topic1_flow()
    if not success:
        sys.exit(1)