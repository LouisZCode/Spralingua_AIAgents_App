"""
Migration script to populate exercise types
These are the different types of exercises available across all topics
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

def populate_exercise_types():
    """Populate the database with exercise type definitions"""
    
    # Define exercise types with their base prompts
    exercise_types = [
        {
            'type_key': 'conversation',
            'name': 'Interactive Conversation',
            'base_prompt_template': """You are a language learning assistant conducting a conversation exercise.
            Engage in natural dialogue while staying within the learner's level. 
            Respond to what the user says, ask follow-up questions, and gently correct major errors.
            Keep your responses concise (1-2 sentences) to encourage more practice from the learner.
            Use only vocabulary and grammar appropriate for their level."""
        },
        {
            'type_key': 'letter_response',
            'name': 'Letter/Email Response',
            'base_prompt_template': """You are helping a learner write a response to a letter or email.
            The learner has received a message and needs to reply appropriately.
            Guide them through the proper format, greetings, and closings for the correspondence.
            Help them express their ideas clearly using level-appropriate language.
            Provide feedback on their writing structure and suggest improvements."""
        },
        {
            'type_key': 'listening_comprehension',
            'name': 'Listening Comprehension',
            'base_prompt_template': """You are conducting a listening comprehension exercise.
            Read a short text or dialogue to the learner, then ask comprehension questions.
            Start with simple yes/no or multiple choice questions, then progress to open-ended ones.
            If the learner struggles, offer to repeat the text or provide hints.
            Focus on understanding main ideas rather than every detail."""
        },
        {
            'type_key': 'fill_blanks',
            'name': 'Fill in the Blanks',
            'base_prompt_template': """You are presenting a fill-in-the-blanks exercise.
            Provide sentences with missing words that the learner must complete.
            The missing words should test specific grammar points or vocabulary from the topic.
            Give feedback on incorrect answers and explain why the correct answer fits.
            Offer hints if the learner is struggling."""
        },
        {
            'type_key': 'role_play',
            'name': 'Role Play Scenario',
            'base_prompt_template': """You are conducting a role-play exercise.
            Take on a specific character role (shopkeeper, receptionist, friend, etc.) for the scenario.
            Stay in character while interacting with the learner.
            Create realistic situations that require the learner to use topic-specific language.
            React naturally to what the learner says while maintaining the scenario context."""
        },
        {
            'type_key': 'pronunciation',
            'name': 'Pronunciation Practice',
            'base_prompt_template': """You are helping with pronunciation practice.
            Focus on specific sounds, word stress, or intonation patterns.
            Provide example words and sentences for the learner to practice.
            Give feedback on common pronunciation mistakes for their language pair.
            Offer tips and techniques for improving pronunciation."""
        },
        {
            'type_key': 'vocabulary_drill',
            'name': 'Vocabulary Practice',
            'base_prompt_template': """You are conducting a vocabulary practice session.
            Present new words from the topic with clear definitions and example sentences.
            Test understanding through various activities: matching, sentences, synonyms/antonyms.
            Help the learner remember words through associations or memory techniques.
            Review previously learned vocabulary to ensure retention."""
        },
        {
            'type_key': 'grammar_focus',
            'name': 'Grammar Exercise',
            'base_prompt_template': """You are teaching a specific grammar point.
            Explain the grammar rule clearly with simple examples.
            Provide practice exercises that gradually increase in difficulty.
            Correct errors and explain why something is grammatically incorrect.
            Connect the grammar to real-life usage within the topic context."""
        },
        {
            'type_key': 'translation',
            'name': 'Translation Practice',
            'base_prompt_template': """You are conducting a translation exercise.
            Provide sentences or short texts for translation between the language pair.
            Focus on natural expression rather than word-for-word translation.
            Explain cultural or idiomatic differences between the languages.
            Help the learner understand when direct translation doesn't work."""
        },
        {
            'type_key': 'question_answer',
            'name': 'Question and Answer Practice',
            'base_prompt_template': """You are practicing questions and answers.
            Ask questions related to the topic and evaluate the learner's responses.
            Teach both how to ask and answer questions properly.
            Focus on question word usage (who, what, where, when, why, how).
            Encourage complete sentence answers rather than single words."""
        }
    ]
    
    with app.app_context():
        try:
            # Check if exercise types already exist
            existing = ExerciseType.query.count()
            if existing > 0:
                print(f"[WARNING] {existing} exercise types already exist. Skipping population.")
                return False
            
            # Add all exercise types
            for type_data in exercise_types:
                exercise_type = ExerciseType(
                    type_key=type_data['type_key'],
                    name=type_data['name'],
                    base_prompt_template=type_data['base_prompt_template']
                )
                db.session.add(exercise_type)
                print(f"[OK] Added exercise type: {type_data['name']} ({type_data['type_key']})")
            
            # Commit all changes
            db.session.commit()
            print(f"\n[OK] Successfully populated {len(exercise_types)} exercise types!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to populate exercise types: {e}")
            return False

if __name__ == '__main__':
    success = populate_exercise_types()
    if not success:
        sys.exit(1)