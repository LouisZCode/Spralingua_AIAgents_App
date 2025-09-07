"""
Migration script to populate A1 topic definitions
Based on the 12-week conversation topics guide
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app

# Import all models to resolve relationships
from models.topic_definition import TopicDefinition
from models.exercise_type import ExerciseType
from models.topic_exercise import TopicExercise
from models.topic_progress import TopicProgress
from models.test_progress import TestProgress

def populate_a1_topics():
    """Populate the database with A1 topic definitions"""
    
    # Define all 12 A1 topics with their prompts
    a1_topics = [
        {
            'topic_number': 1,
            'title_key': 'who_are_you',
            'subtopics': ['Greetings', 'Introducing yourself', 'Saying goodbye'],
            'conversation_contexts': [
                'Meeting someone for the first time',
                'Casual greeting with a friend',
                'Formal introduction at work'
            ],
            'llm_prompt_template': """You are having a first meeting conversation at A1 level. 
            Start with an appropriate greeting for the time of day. Introduce yourself with a simple name and ask for theirs.
            Use only present simple tense and basic vocabulary. Expected structures: 'Hello, I am...', 'What is your name?', 
            'Nice to meet you', 'How are you?', 'I am fine, thank you'. 
            Keep sentences short and clear. If the user makes mistakes, gently correct them using simpler words.
            End conversations with appropriate farewells like 'Goodbye', 'See you later', 'Have a nice day'."""
        },
        {
            'topic_number': 2,
            'title_key': 'what_do_you_do',
            'subtopics': ['Meeting someone', 'Professions', 'Saying where you come from'],
            'conversation_contexts': [
                'Talking about your job',
                'Asking about someone\'s profession',
                'Discussing where you live and work'
            ],
            'llm_prompt_template': """You are having a conversation about professions and origins at A1 level.
            Ask and answer about jobs using 'What do you do?' and 'I am a...'. Include common professions like teacher,
            doctor, student, engineer. Ask 'Where are you from?' and answer with 'I am from [country/city]'.
            Use simple present tense only. Vocabulary should include basic job titles and country names.
            Help the user practice: 'I work in...', 'I live in...', 'I come from...'."""
        },
        {
            'topic_number': 3,
            'title_key': 'know_your_abc',
            'subtopics': ['Spelling your name and surnames', 'Say where you are going', 'Verify the name of a street'],
            'conversation_contexts': [
                'Spelling names for registration',
                'Giving directions with street names',
                'Confirming addresses'
            ],
            'llm_prompt_template': """You are practicing spelling and the alphabet at A1 level.
            Practice spelling names letter by letter. Use the phonetic alphabet if helpful (A for Apple, B for Boy).
            Ask 'How do you spell that?' and 'Can you spell your name?'. Practice street names and addresses.
            Include: 'Where are you going?' with answers like 'I am going to [place]'.
            Keep vocabulary simple and focus on clear pronunciation of letters."""
        },
        {
            'topic_number': 4,
            'title_key': 'can_you_spell_it',
            'subtopics': ['Confirm ticket/booking information', 'Check for package information', 'Buying things in a pharmacy'],
            'conversation_contexts': [
                'Confirming a hotel reservation',
                'Checking flight details',
                'Asking for medicine at a pharmacy'
            ],
            'llm_prompt_template': """You are practicing confirmation and verification conversations at A1 level.
            Use phrases like 'Can you confirm...?', 'Is this correct?', 'Let me check...'.
            For pharmacy contexts, use: 'I need...', 'Do you have...?', 'How much is...?'.
            Practice booking confirmations: 'My reservation number is...', 'The booking is for [date]'.
            Include basic medical vocabulary: headache, cold, medicine, tablets."""
        },
        {
            'topic_number': 5,
            'title_key': 'whats_the_number',
            'subtopics': ['Talk about age', 'Confirm general information', 'Everyday use of numbers and figures'],
            'conversation_contexts': [
                'Discussing ages in a family',
                'Sharing phone numbers',
                'Talking about quantities'
            ],
            'llm_prompt_template': """You are practicing numbers and ages at A1 level.
            Focus on numbers 1-100. Practice: 'How old are you?', 'I am [number] years old'.
            Include phone numbers: 'My phone number is...'. Practice quantities: 'I have [number] [items]'.
            Use numbers in daily contexts: addresses, prices, times, dates.
            Keep calculations simple and help with number pronunciation."""
        },
        {
            'topic_number': 6,
            'title_key': 'how_much_is_it',
            'subtopics': ['Buying things', 'Asking for prices', 'Talk about cheap and expensive things'],
            'conversation_contexts': [
                'Shopping at a market',
                'Buying clothes',
                'Discussing prices at a restaurant'
            ],
            'llm_prompt_template': """You are practicing shopping and prices at A1 level.
            Key phrases: 'How much is this?', 'How much does it cost?', 'It costs [amount]'.
            Use currency appropriately. Practice: 'It\'s expensive/cheap', 'Can I pay by card/cash?'.
            Include shopping vocabulary: buy, sell, pay, change, receipt.
            Help with price negotiations: 'Is there a discount?', 'I\'ll take it'."""
        },
        {
            'topic_number': 7,
            'title_key': 'whats_your_address',
            'subtopics': ['Talk about where you come from', 'Talk about where you live', 'Asking someone for their address'],
            'conversation_contexts': [
                'Giving your home address',
                'Describing your neighborhood',
                'Asking for delivery address'
            ],
            'llm_prompt_template': """You are practicing addresses and locations at A1 level.
            Practice: 'What\'s your address?', 'I live at [number] [street name]'.
            Include: 'I live in a house/apartment', 'My neighborhood is quiet/busy'.
            Use prepositions: in, on, at, near, next to. Describe basic locations: 'near the park', 'in the city center'.
            Keep descriptions simple and focus on essential address components."""
        },
        {
            'topic_number': 8,
            'title_key': 'more_about_you',
            'subtopics': ['Exchanging personal information', 'Asking someone to contact you', 'Interviewing someone for their personal details'],
            'conversation_contexts': [
                'Filling out a form together',
                'Exchanging contact information',
                'Simple job interview questions'
            ],
            'llm_prompt_template': """You are practicing personal information exchange at A1 level.
            Cover: email addresses, phone numbers, date of birth, nationality.
            Practice: 'Can I have your email?', 'My email is...', 'When is your birthday?'.
            Include marital status: single, married. Use: 'Please contact me at...'.
            Keep forms simple and help with spelling of email addresses."""
        },
        {
            'topic_number': 9,
            'title_key': 'what_are_they_like',
            'subtopics': ['Describing your family', 'Describing what friends and family are like', 'Describing what friends and family like'],
            'conversation_contexts': [
                'Talking about family members',
                'Describing a friend\'s personality',
                'Discussing hobbies and interests'
            ],
            'llm_prompt_template': """You are practicing family and descriptions at A1 level.
            Use basic adjectives: tall, short, young, old, nice, friendly.
            Family vocabulary: mother, father, sister, brother, son, daughter.
            Practice: 'My sister is tall', 'He is very friendly', 'They like music'.
            Include simple likes/dislikes: 'She likes reading', 'He doesn\'t like sports'."""
        },
        {
            'topic_number': 10,
            'title_key': 'what_do_they_do',
            'subtopics': ['Talking about family and relatives', 'Keeping in touch with friends and family', 'Describing what friends and family do'],
            'conversation_contexts': [
                'Discussing family members\' jobs',
                'Talking about how you communicate',
                'Describing daily routines'
            ],
            'llm_prompt_template': """You are practicing family activities and communication at A1 level.
            Discuss jobs: 'My father is a teacher', 'My mother works in a bank'.
            Communication: 'I call my family every week', 'We text every day'.
            Simple present for routines: 'She goes to school', 'He works in an office'.
            Keep descriptions simple and focus on regular activities."""
        },
        {
            'topic_number': 11,
            'title_key': 'what_time_is_it',
            'subtopics': ['Asking for and telling time', 'Talking about days of the week', 'Describing seasons and weather'],
            'conversation_contexts': [
                'Asking for the time',
                'Planning weekly activities',
                'Discussing weather and seasons'
            ],
            'llm_prompt_template': """You are practicing time, days, and weather at A1 level.
            Time: 'What time is it?', 'It\'s three o\'clock', 'It\'s half past two'.
            Days: Monday through Sunday, 'What day is today?', 'Today is Monday'.
            Weather: 'It\'s sunny/rainy/cold/hot', 'I like summer/winter'.
            Seasons: spring, summer, autumn/fall, winter. Keep time expressions simple."""
        },
        {
            'topic_number': 12,
            'title_key': 'when_is_it',
            'subtopics': ['Talk about your birthday', 'Making appointments', 'Talk about plans for the week'],
            'conversation_contexts': [
                'Discussing birthdays and celebrations',
                'Scheduling a meeting',
                'Planning weekend activities'
            ],
            'llm_prompt_template': """You are practicing dates and plans at A1 level.
            Dates: 'When is your birthday?', 'My birthday is on [date]'.
            Months: January through December. Ordinal numbers for dates: first, second, third.
            Making plans: 'Can we meet on Monday?', 'I\'m free on Friday'.
            Future with 'going to': 'I\'m going to visit my family', 'We\'re going to have a party'."""
        }
    ]
    
    with app.app_context():
        try:
            # Check if A1 topics already exist
            existing = TopicDefinition.query.filter_by(level='A1').count()
            if existing > 0:
                print(f"[WARNING] {existing} A1 topics already exist. Skipping population.")
                return False
            
            # Add all topics
            for topic_data in a1_topics:
                topic = TopicDefinition(
                    level='A1',
                    topic_number=topic_data['topic_number'],
                    title_key=topic_data['title_key'],
                    subtopics=topic_data['subtopics'],
                    conversation_contexts=topic_data['conversation_contexts'],
                    llm_prompt_template=topic_data['llm_prompt_template']
                )
                db.session.add(topic)
                print(f"[OK] Added A1 Topic {topic_data['topic_number']}: {topic_data['title_key']}")
            
            # Commit all changes
            db.session.commit()
            print(f"\n[OK] Successfully populated {len(a1_topics)} A1 topics!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to populate A1 topics: {e}")
            return False

if __name__ == '__main__':
    success = populate_a1_topics()
    if not success:
        sys.exit(1)