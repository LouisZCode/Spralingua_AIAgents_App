"""
Migration script to create user_progress table
Run this script to add the user_progress table to your database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from models.user_progress import UserProgress

def create_user_progress_table():
    """Create the user_progress table in the database"""
    with app.app_context():
        # Create the table
        db.create_all()
        print("[OK] user_progress table created successfully")
        
        # Verify the table exists
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'user_progress' in tables:
            print("[OK] Verified: user_progress table exists")
            
            # Get column info
            columns = inspector.get_columns('user_progress')
            print("\nTable structure:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        else:
            print("[ERROR] user_progress table was not created")

if __name__ == '__main__':
    create_user_progress_table()