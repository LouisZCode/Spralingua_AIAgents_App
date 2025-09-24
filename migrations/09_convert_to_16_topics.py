# Migration to convert to 16-topic structure with integrated tests
# Tests at positions 4, 8, 12, 16

import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.topic_definition import TopicDefinition
from app import app
import json

def renumber_existing_topics():
    """Renumber existing topics to make room for tests."""
    with app.app_context():
        # Map old topic numbers to new ones
        # Old 4-6 become 5-7, old 7-9 become 9-11, old 10-12 become 13-15
        renumbering = {
            4: 5,   # can_you_spell_it
            5: 6,   # whats_the_number
            6: 7,   # how_much_is_it
            7: 9,   # whats_your_address
            8: 10,  # more_about_you
            9: 11,  # what_are_they_like
            10: 13, # what_do_they_do
            11: 14, # what_time_is_it
            12: 15  # when_is_it
        }

        # First, temporarily move topics to high numbers to avoid conflicts
        for old_num in sorted(renumbering.keys(), reverse=True):
            topic = TopicDefinition.query.filter_by(level='A1', topic_number=old_num).first()
            if topic:
                topic.topic_number = old_num + 100  # Temporary high number
                print(f"Temporarily moved topic {old_num} to {old_num + 100}")

        db.session.commit()

        # Now move them to their final positions
        for old_num, new_num in renumbering.items():
            topic = TopicDefinition.query.filter_by(level='A1', topic_number=old_num + 100).first()
            if topic:
                topic.topic_number = new_num
                print(f"Moved topic from position {old_num} to {new_num}: {topic.title_key}")

        db.session.commit()
        print("Topic renumbering complete!")

def create_test_topics():
    """Create 4 test topics at positions 4, 8, 12, 16."""
    with app.app_context():
        tests = [
            {
                'position': 4,
                'title': 'test_checkpoint_1',
                'topics_covered': [1, 2, 3],
                'topics_names': ['greetings/introductions', 'professions/origins', 'spelling/alphabet'],
                'scenario': 'International Language Exchange Event'
            },
            {
                'position': 8,
                'title': 'test_checkpoint_2',
                'topics_covered': [5, 6, 7],
                'topics_names': ['confirmations/pharmacy', 'numbers/quantities', 'shopping/prices'],
                'scenario': 'Hotel Check-in and Gift Shop'
            },
            {
                'position': 12,
                'title': 'test_checkpoint_3',
                'topics_covered': [9, 10, 11],
                'topics_names': ['addresses/locations', 'personal information', 'family descriptions'],
                'scenario': 'Community Center Registration'
            },
            {
                'position': 16,
                'title': 'test_final',
                'topics_covered': [13, 14, 15],
                'topics_names': ['family activities', 'time/weather', 'dates/appointments'],
                'scenario': 'Family Gathering Planning'
            }
        ]

        for test in tests:
            # Check if test already exists
            existing = TopicDefinition.query.filter_by(level='A1', topic_number=test['position']).first()
            if existing:
                print(f"Test at position {test['position']} already exists, skipping...")
                continue

            # Create integrated prompt that tests all 3 topics
            topics_str = ', '.join(test['topics_names'])
            prompt = f"""You are conducting a checkpoint test for {test['scenario']}.

## Test Parameters
- This is a TEST combining topics: {topics_str}
- Number of exchanges: 10 (double the normal length)
- Student must demonstrate knowledge from ALL THREE topics
- Passing threshold: 20% accuracy

## Integration Instructions
Start with elements from the first topic, naturally transition through the second topic, and conclude incorporating the third topic. The conversation should feel like one cohesive scenario, not three separate mini-conversations.

## Scenario Context
{test['scenario']}: Create a natural scenario where all three topics flow together seamlessly.

## CRITICAL TEST RULES:
1. You MUST test elements from ALL THREE topics during the conversation
2. Distribute the topic coverage evenly across the 10 exchanges
3. Make smooth, natural transitions between topics
4. Maintain the scenario context throughout
5. Gradually increase complexity as the test progresses
6. Be encouraging but maintain test standards
7. After 10 exchanges, provide a brief summary of the student's performance

Remember: This is a TEST, not practice. Assess the student's ability to integrate knowledge from multiple topics."""

            test_topic = TopicDefinition(
                level='A1',
                topic_number=test['position'],
                title_key=test['title'],
                subtopics=json.dumps(test['topics_names']),
                conversation_contexts=json.dumps([test['scenario']]),
                llm_prompt_template=prompt,
                word_limit=30,  # Double the A1 base of 15
                opening_phrases=json.dumps({
                    'english': [f"Hello! Welcome to your checkpoint test covering topics {test['topics_covered'][0]}-{test['topics_covered'][2]}. Let's begin with {test['scenario']}."],
                    'german': [f"Hallo! Willkommen zu Ihrem Checkpoint-Test für die Themen {test['topics_covered'][0]}-{test['topics_covered'][2]}. Beginnen wir mit {test['scenario']}."],
                    'spanish': [f"¡Hola! Bienvenido a tu prueba de control de los temas {test['topics_covered'][0]}-{test['topics_covered'][2]}. Empecemos con {test['scenario']}."],
                    'portuguese': [f"Olá! Bem-vindo ao seu teste de verificação dos tópicos {test['topics_covered'][0]}-{test['topics_covered'][2]}. Vamos começar com {test['scenario']}."]
                }),
                required_vocabulary=json.dumps([]),
                conversation_flow=json.dumps({
                    'exchanges': 10,
                    'structure': f'Integrated test covering {topics_str}'
                }),
                number_of_exchanges=10,  # Double the normal 5
                topic_specific_rules=f'TEST MODE: Assess all three topics ({topics_str}) in an integrated manner',
                scenario_template=f'{test["scenario"]} - Testing topics {test["topics_covered"]}'
            )

            db.session.add(test_topic)
            print(f"Created test at position {test['position']}: {test['title']}")

        db.session.commit()
        print("All test topics created!")

def update_topic_progress():
    """Update topic_progress records to include new topic numbers."""
    with app.app_context():
        from models.topic_progress import TopicProgress
        from models.user_progress import UserProgress

        # Get all user progress records
        user_progresses = UserProgress.query.all()

        for up in user_progresses:
            # Check which topics need progress records
            for topic_num in [4, 8, 12, 16]:  # Test positions
                existing = TopicProgress.query.filter_by(
                    user_progress_id=up.id,
                    topic_number=topic_num
                ).first()

                if not existing:
                    # Create progress record for test topic
                    progress = TopicProgress(
                        user_progress_id=up.id,
                        topic_number=topic_num,
                        total_exercises=2  # Casual chat and email writing
                    )
                    db.session.add(progress)
                    print(f"Added test progress for user {up.user_id}, topic {topic_num}")

        db.session.commit()
        print("Topic progress updated for all users!")

if __name__ == "__main__":
    print("Starting 16-topic migration...")
    print("Step 1: Renumbering existing topics...")
    renumber_existing_topics()

    print("\nStep 2: Creating test topics...")
    create_test_topics()

    print("\nStep 3: Updating user progress records...")
    update_topic_progress()

    print("\nMigration complete! Now have 16 topics with tests at positions 4, 8, 12, 16")