"""
Migration script to update A1 Topic 1 conversation flow back to 5 exchanges
Simplifying the conversation flow for better user experience
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from models.topic_definition import TopicDefinition

def update_topic1_to_5_exchanges():
    """Update A1 Topic 1 to have 5 exchanges instead of 6"""

    # Updated conversation flow for 5 exchanges
    # Combining the location questions into one exchange
    updated_flow = [
        "Greeting + name introduction + ask their name",
        "Nice to meet you + ask where from (country/city)",
        "React to location + say where you're from",
        "Ask how they are",
        "Share one simple hobby + farewell"
    ]

    # Keep the same opening phrases
    opening_phrases = {
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

            print(f"[INFO] Current number of exchanges: {topic.number_of_exchanges}")
            print(f"[INFO] Current flow: {topic.conversation_flow}")

            # Update conversation flow
            topic.conversation_flow = updated_flow

            # Update number of exchanges from 6 to 5
            topic.number_of_exchanges = 5

            # Keep the opening phrases
            topic.opening_phrases = opening_phrases

            # Update the topic-specific rules to reflect 5 exchanges
            topic.topic_specific_rules = """STRICT RULES FOR A1 TOPIC 1:
- Maximum 15 words per response
- Use ONLY present simple tense
- NO complex sentences (no 'and' chains, no 'because', no 'that')
- Ask ONE question at a time
- Wait for response before next question
- When student says their location, be specific in your response
- Keep all questions simple and natural
- In the final exchange, share your hobby and say goodbye"""

            # Commit changes
            db.session.commit()

            print("[SUCCESS] Updated A1 Topic 1 conversation flow:")
            print(f"- Changed exchanges from 6 to 5")
            print("- Simplified flow by combining location questions")
            print("- Updated flow:")
            for i, step in enumerate(updated_flow, 1):
                print(f"  {i}. {step}")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to update Topic 1: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("Migration: Update A1 Topic 1 to 5 exchanges")
    print("=" * 60)
    print("This migration will:")
    print("1. Update A1 Topic 1 from 6 to 5 exchanges")
    print("2. Simplify the conversation flow")
    print("3. Update topic-specific rules")
    print("-" * 60)

    if update_topic1_to_5_exchanges():
        print("\n[SUCCESS] Migration completed!")
        print("A1 Topic 1 now has 5 exchanges with simplified flow.")
    else:
        print("\n[ERROR] Migration failed. Please check the error messages above.")