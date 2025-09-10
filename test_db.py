from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import models (after db is initialized)
from models.user import User

def test_database():
    """Test database connection and operations"""
    with app.app_context():
        try:
            # Test connection
            result = db.session.execute(db.text("SELECT current_database(), current_user"))
            row = result.fetchone()
            print(f"[OK] Connected to database: {row[0]} as user: {row[1]}")
            
            # Create a test user
            test_email = "test@spralingua.com"
            
            # Check if test user already exists
            existing_user = User.query.filter_by(email=test_email).first()
            if existing_user:
                print(f"[OK] Test user already exists: {existing_user}")
                # Update progress level
                existing_user.update_progress(existing_user.progress_level + 1)
                db.session.commit()
                print(f"  Updated progress to level {existing_user.progress_level}")
            else:
                # Create new test user
                test_user = User(
                    email=test_email,
                    password="testpass123",
                    progress_level=1
                )
                db.session.add(test_user)
                db.session.commit()
                print(f"[OK] Created test user: {test_user}")
            
            # Test password verification
            user = User.query.filter_by(email=test_email).first()
            if user.check_password("testpass123"):
                print("[OK] Password verification works!")
            else:
                print("[FAIL] Password verification failed!")
            
            # List all users
            all_users = User.query.all()
            print(f"\n[OK] Total users in database: {len(all_users)}")
            for user in all_users:
                print(f"  - {user}")
            
            print("\n[SUCCESS] Database test completed successfully!")
            
        except Exception as e:
            print(f"[ERROR] Database test failed: {e}")

if __name__ == '__main__':
    test_database()