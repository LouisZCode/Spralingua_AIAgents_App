"""
Migration script to enhance topic_definitions table with new columns
and migrate data from a1_topic_scripts.yaml
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from models.topic_definition import TopicDefinition
from sqlalchemy import text

def enhance_topic_definitions():
    """Add new columns to topic_definitions and populate with A1 data"""
    
    # A1 topic enhancements (migrated from a1_topic_scripts.yaml)
    a1_enhancements = {
        1: {  # who_are_you
            'word_limit': 15,
            'opening_phrases': {
                'german': "Hallo! Ich bin Harry. Wie heißt du?",
                'spanish': "¡Hola! Soy Harry. ¿Cómo te llamas?",
                'portuguese': "Olá! Eu sou o Harry. Como te chamas?",
                'english': "Hello! I'm Harry. What's your name?"
            },
            'required_vocabulary': [
                "hello", "hi", "good morning/afternoon/evening",
                "I am", "my name is", "nice to meet you",
                "What's your name?", "Where are you from?", "How are you?",
                "I'm fine", "thank you", "and you?"
            ],
            'conversation_flow': [
                "Greeting + name introduction + ask their name",
                "Nice to meet you + ask where from",
                "React to location + say where you're from",
                "Ask how they are",
                "Share one simple hobby (snowboarding)"
            ],
            'topic_specific_rules': """STRICT RULES FOR A1 TOPIC 1:
- Maximum 15 words per response
- Use ONLY present simple tense
- NO complex sentences (no 'and' chains, no 'because', no 'that')
- Ask ONE question at a time
- Wait for response before next question"""
        },
        2: {  # what_do_you_do
            'word_limit': 15,
            'opening_phrases': {
                'german': "Hallo! Was machst du beruflich?",
                'spanish': "¡Hola! ¿A qué te dedicas?",
                'portuguese': "Olá! O que fazes?",
                'english': "Hello! What do you do?"
            },
            'required_vocabulary': [
                "teacher", "student", "doctor", "engineer", "worker",
                "office", "school", "hospital", "shop",
                "work", "teach", "study", "help"
            ],
            'conversation_flow': [
                "Ask about their profession",
                "Share your job (snowboard instructor)",
                "Ask where they work",
                "Share where you work",
                "Ask if they like their job"
            ]
        },
        3: {  # know_your_abc
            'word_limit': 20,
            'opening_phrases': {
                'german': "Hallo! Wie schreibt man deinen Namen?",
                'spanish': "¡Hola! ¿Cómo se escribe tu nombre?",
                'portuguese': "Olá! Como se escreve o teu nome?",
                'english': "Hello! How do you spell your name?"
            },
            'required_vocabulary': [
                "spell", "letter", "alphabet",
                "How do you spell?", "Can you spell?",
                "street", "address", "email"
            ],
            'conversation_flow': [
                "Ask them to spell their name",
                "Spell your name: H-A-R-R-Y",
                "Ask for their email",
                "Practice spelling simple words"
            ]
        },
        4: {  # can_you_spell_it
            'word_limit': 20,
            'opening_phrases': {
                'german': "Hallo! Brauchst du etwas aus der Apotheke?",
                'spanish': "¡Hola! ¿Necesitas algo de la farmacia?",
                'portuguese': "Olá! Precisas de algo da farmácia?",
                'english': "Hello! Do you need something from the pharmacy?"
            },
            'required_vocabulary': [
                "tablets", "medicine", "headache",
                "Is that correct?", "Let me check",
                "reservation", "booking", "confirm"
            ],
            'conversation_flow': [
                "Ask what they need",
                "Confirm the item",
                "Ask for quantity",
                "Confirm the order",
                "Give price"
            ]
        },
        5: {  # whats_the_number
            'word_limit': 15,
            'opening_phrases': {
                'german': "Hallo! Wie alt bist du?",
                'spanish': "¡Hola! ¿Cuántos años tienes?",
                'portuguese': "Olá! Quantos anos tens?",
                'english': "Hello! How old are you?"
            },
            'required_vocabulary': [
                "numbers 1-100", "years old",
                "phone number", "How old?", "How many?"
            ],
            'conversation_flow': [
                "Ask their age",
                "Share your age",
                "Ask for phone number",
                "Share yours (digit by digit)",
                "Practice counting something"
            ]
        },
        6: {  # how_much_is_it
            'word_limit': 20,
            'opening_phrases': {
                'german': "Hallo! Was möchtest du kaufen?",
                'spanish': "¡Hola! ¿Qué quieres comprar?",
                'portuguese': "Olá! O que queres comprar?",
                'english': "Hello! What do you want to buy?"
            },
            'required_vocabulary': [
                "How much?", "It costs", "euros", "dollars",
                "buy", "sell", "cheap", "expensive",
                "card", "cash", "change", "receipt"
            ],
            'conversation_flow': [
                "Ask what they want to buy",
                "Ask about size/color",
                "Give price",
                "Ask payment method",
                "Complete transaction"
            ]
        },
        7: {  # whats_your_address
            'word_limit': 25,
            'opening_phrases': {
                'german': "Hallo! Wo wohnst du?",
                'spanish': "¡Hola! ¿Dónde vives?",
                'portuguese': "Olá! Onde moras?",
                'english': "Hello! Where do you live?"
            },
            'required_vocabulary': [
                "street", "number", "city", "country",
                "house", "apartment", "near", "next to",
                "What's your address?", "I live at"
            ],
            'conversation_flow': [
                "Ask where they live",
                "Share your city",
                "Ask for specific address",
                "Describe your neighborhood",
                "Ask about their neighborhood"
            ]
        },
        8: {  # more_about_you
            'word_limit': 25,
            'opening_phrases': {
                'german': "Hallo! Erzähl mir von dir!",
                'spanish': "¡Hola! ¡Cuéntame sobre ti!",
                'portuguese': "Olá! Fala-me sobre ti!",
                'english': "Hello! Tell me about yourself!"
            },
            'required_vocabulary': [
                "email", "birthday", "nationality",
                "single", "married", "contact",
                "Can I have your?", "My email is"
            ],
            'conversation_flow': [
                "Ask for basic info",
                "Share your nationality",
                "Ask for email",
                "Ask about birthday",
                "Exchange contact info"
            ]
        },
        9: {  # what_are_they_like
            'word_limit': 20,
            'opening_phrases': {
                'german': "Hallo! Hast du Geschwister?",
                'spanish': "¡Hola! ¿Tienes hermanos?",
                'portuguese': "Olá! Tens irmãos?",
                'english': "Hello! Do you have siblings?"
            },
            'required_vocabulary': [
                "mother", "father", "sister", "brother",
                "tall", "short", "nice", "friendly",
                "young", "old", "like", "don't like"
            ],
            'conversation_flow': [
                "Ask about siblings",
                "Describe your family",
                "Ask about their parents",
                "Share family hobbies",
                "Ask what family likes"
            ]
        },
        10: {  # what_do_they_do
            'word_limit': 25,
            'opening_phrases': {
                'german': "Hallo! Was macht deine Familie?",
                'spanish': "¡Hola! ¿Qué hace tu familia?",
                'portuguese': "Olá! O que faz a tua família?",
                'english': "Hello! What does your family do?"
            },
            'required_vocabulary': [
                "family jobs", "works in", "goes to school",
                "call", "text", "visit", "every day", "weekend"
            ],
            'conversation_flow': [
                "Ask about family jobs",
                "Share parent's job",
                "Ask how often they meet",
                "Share communication habits",
                "Ask about family activities"
            ]
        },
        11: {  # what_time_is_it
            'word_limit': 20,
            'opening_phrases': {
                'german': "Hallo! Wie spät ist es?",
                'spanish': "¡Hola! ¿Qué hora es?",
                'portuguese': "Olá! Que horas são?",
                'english': "Hello! What time is it?"
            },
            'required_vocabulary': [
                "o'clock", "half past", "quarter",
                "Monday-Sunday", "today", "tomorrow",
                "sunny", "rainy", "cold", "hot",
                "spring", "summer", "autumn", "winter"
            ],
            'conversation_flow': [
                "Ask the time",
                "Ask about today's day",
                "Talk about weather",
                "Ask favorite season",
                "Share weekend plans"
            ]
        },
        12: {  # when_is_it
            'word_limit': 25,
            'opening_phrases': {
                'german': "Hallo! Wann hast du Geburtstag?",
                'spanish': "¡Hola! ¿Cuándo es tu cumpleaños?",
                'portuguese': "Olá! Quando é o teu aniversário?",
                'english': "Hello! When is your birthday?"
            },
            'required_vocabulary': [
                "January-December", "first", "second", "third",
                "birthday", "party", "celebrate",
                "going to", "next week", "weekend"
            ],
            'conversation_flow': [
                "Ask about birthday",
                "Share your birthday",
                "Ask about celebrations",
                "Ask about weekend plans",
                "Share your plans"
            ]
        }
    }
    
    with app.app_context():
        try:
            # First, add the new columns if they don't exist
            # We'll use raw SQL for ALTER TABLE since SQLAlchemy doesn't handle this well
            with db.engine.connect() as conn:
                # Check if columns exist first
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='topic_definitions' 
                    AND column_name IN ('word_limit', 'opening_phrases', 'required_vocabulary', 
                                       'conversation_flow', 'number_of_exchanges', 'topic_specific_rules')
                """))
                existing_columns = [row[0] for row in result]
                
                # Add columns that don't exist
                if 'word_limit' not in existing_columns:
                    conn.execute(text("ALTER TABLE topic_definitions ADD COLUMN word_limit INTEGER"))
                    conn.commit()
                    print("[OK] Added word_limit column")
                
                if 'opening_phrases' not in existing_columns:
                    conn.execute(text("ALTER TABLE topic_definitions ADD COLUMN opening_phrases JSON"))
                    conn.commit()
                    print("[OK] Added opening_phrases column")
                
                if 'required_vocabulary' not in existing_columns:
                    conn.execute(text("ALTER TABLE topic_definitions ADD COLUMN required_vocabulary JSON"))
                    conn.commit()
                    print("[OK] Added required_vocabulary column")
                
                if 'conversation_flow' not in existing_columns:
                    conn.execute(text("ALTER TABLE topic_definitions ADD COLUMN conversation_flow JSON"))
                    conn.commit()
                    print("[OK] Added conversation_flow column")
                
                if 'number_of_exchanges' not in existing_columns:
                    conn.execute(text("ALTER TABLE topic_definitions ADD COLUMN number_of_exchanges INTEGER DEFAULT 5"))
                    conn.commit()
                    print("[OK] Added number_of_exchanges column")
                
                if 'topic_specific_rules' not in existing_columns:
                    conn.execute(text("ALTER TABLE topic_definitions ADD COLUMN topic_specific_rules TEXT"))
                    conn.commit()
                    print("[OK] Added topic_specific_rules column")
            
            # Now update A1 topics with the enhanced data
            for topic_num, enhancements in a1_enhancements.items():
                topic = TopicDefinition.query.filter_by(level='A1', topic_number=topic_num).first()
                if topic:
                    topic.word_limit = enhancements.get('word_limit')
                    topic.opening_phrases = enhancements.get('opening_phrases')
                    topic.required_vocabulary = enhancements.get('required_vocabulary')
                    topic.conversation_flow = enhancements.get('conversation_flow')
                    topic.number_of_exchanges = enhancements.get('number_of_exchanges', 5)
                    topic.topic_specific_rules = enhancements.get('topic_specific_rules')
                    print(f"[OK] Enhanced A1 Topic {topic_num}")
            
            db.session.commit()
            print(f"\n[SUCCESS] Successfully enhanced topic_definitions table and migrated A1 data!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to enhance topic_definitions: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = enhance_topic_definitions()
    if not success:
        sys.exit(1)