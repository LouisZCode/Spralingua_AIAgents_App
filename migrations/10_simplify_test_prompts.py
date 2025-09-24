# Migration to simplify test prompts - make them natural like regular topics
# Remove excessive meta-information and testing language

import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_definition import TopicDefinition
from app import app

def update_test_prompts():
    """Update test prompts to be simpler and more natural."""
    with app.app_context():

        # Define the new simplified prompts for each test
        test_prompts = {
            4: """You are at an international language exchange event at A1 level.
You will meet someone new, talk about professions and origins, and practice spelling names and emails.
Start with greetings and introductions. Ask about their job and where they're from. Practice spelling when exchanging contact information.
Use simple vocabulary: 'Hello, I am...', 'What do you do?', 'I work as...', 'Where are you from?', 'How do you spell that?'.
Keep sentences short and help the student practice all these elements naturally in the conversation.""",

            8: """You are at a hotel check-in desk and gift shop at A1 level.
You will confirm a reservation, discuss room numbers and prices, and help with shopping.
Start by confirming booking details. Use numbers for room, floor, and prices. End with buying something from the gift shop.
Use phrases like: 'Can you confirm...?', 'Room number is...', 'That costs...', 'How much is this?', 'I would like to buy...'.
Keep vocabulary simple and help the student practice confirmations, numbers, and shopping naturally.""",

            12: """You are at a community center registration desk at A1 level.
You will help someone register by collecting their address, personal information, and family details.
Start by asking where they live. Then get their personal details like email and birthday. Finally ask about their family members.
Use phrases like: 'Where do you live?', 'What's your email?', 'When is your birthday?', 'How many people in your family?', 'What do they do?'.
Keep the conversation natural and help the student share all this information simply.""",

            16: """You are planning a family gathering at A1 level.
You will discuss what family members do, check times and weather, and set a date for the event.
Start by talking about family activities and jobs. Then discuss the best time and check the weather. Finally agree on a date.
Use phrases like: 'My sister works as...', 'What time is good?', 'The weather will be...', 'Let's meet on [date]', 'My birthday is...'.
Keep everything simple and help the student plan this family event naturally."""
        }

        # Also update the topic_specific_rules to be simpler
        test_rules = {
            4: "Practice greetings, professions, and spelling in a natural conversation flow.",
            8: "Practice confirmations, numbers, and shopping in a hotel context.",
            12: "Practice addresses, personal info, and family descriptions for registration.",
            16: "Practice family activities, time/weather, and dates while planning an event."
        }

        # Update each test topic
        for topic_num, new_prompt in test_prompts.items():
            topic = TopicDefinition.query.filter_by(level='A1', topic_number=topic_num).first()

            if topic:
                old_length = len(topic.llm_prompt_template)
                topic.llm_prompt_template = new_prompt
                topic.topic_specific_rules = test_rules[topic_num]
                new_length = len(new_prompt)

                print(f"Updated Topic {topic_num} ({topic.title_key}):")
                print(f"  - Old prompt length: {old_length} chars")
                print(f"  - New prompt length: {new_length} chars")
                print(f"  - Reduction: {old_length - new_length} chars ({int((1 - new_length/old_length) * 100)}%)")
            else:
                print(f"WARNING: Topic {topic_num} not found")

        db.session.commit()
        print("\nAll test prompts simplified successfully!")
        print("Tests now use natural conversation flow without explicit testing language.")

if __name__ == "__main__":
    print("Starting test prompt simplification...")
    update_test_prompts()
    print("\nMigration complete!")