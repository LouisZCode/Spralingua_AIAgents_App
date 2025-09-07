"""
Migration script to create topic/exercise/test system tables
Run this script to add all topic-related tables to your database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app

# Import all new models
from models.topic_definition import TopicDefinition
from models.exercise_type import ExerciseType
from models.topic_exercise import TopicExercise
from models.topic_progress import TopicProgress
from models.test_progress import TestProgress

def create_topic_system_tables():
    """Create all topic system tables in the database"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("[OK] Creating topic system tables...")
        
        # Verify each table exists
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'topic_definitions',
            'exercise_types', 
            'topic_exercises',
            'topic_progress',
            'test_progress'
        ]
        
        print("\nChecking tables:")
        all_created = True
        for table in required_tables:
            if table in tables:
                print(f"  [OK] {table} table created")
                
                # Show table structure
                columns = inspector.get_columns(table)
                print(f"      Columns: {', '.join([col['name'] for col in columns])}")
            else:
                print(f"  [ERROR] {table} table was not created")
                all_created = False
        
        if all_created:
            print("\n[OK] All topic system tables created successfully!")
        else:
            print("\n[ERROR] Some tables were not created. Please check for errors.")
        
        return all_created

if __name__ == '__main__':
    success = create_topic_system_tables()
    if not success:
        sys.exit(1)