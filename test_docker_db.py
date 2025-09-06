import subprocess
import json

def test_docker_database():
    """Test database operations using Docker PostgreSQL"""
    
    print("Testing Docker PostgreSQL connection...")
    
    # Test connection
    result = subprocess.run(
        ['docker', 'exec', 'gta-postgres', 'psql', '-U', 'dev', '-d', 'spralingua_dev', '-t', '-c', 
         "SELECT current_database(), current_user;"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        db_info = result.stdout.strip()
        print(f"Connected to Docker PostgreSQL: {db_info}")
    else:
        print(f"Failed to connect: {result.stderr}")
        return
    
    # Check if test user exists
    result = subprocess.run(
        ['docker', 'exec', 'gta-postgres', 'psql', '-U', 'dev', '-d', 'spralingua_dev', '-t', '-c', 
         "SELECT email, progress_level FROM users WHERE email = 'test@spralingua.com';"],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print(f"Test user exists: {result.stdout.strip()}")
    else:
        # Create test user (password will be hashed by the app later)
        result = subprocess.run(
            ['docker', 'exec', 'gta-postgres', 'psql', '-U', 'dev', '-d', 'spralingua_dev', '-c', 
             "INSERT INTO users (email, password_hash, progress_level) VALUES ('test@spralingua.com', 'placeholder_hash', 1) RETURNING id, email, progress_level;"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Created test user: {result.stdout}")
        else:
            print(f"Failed to create user: {result.stderr}")
    
    # List all users
    result = subprocess.run(
        ['docker', 'exec', 'gta-postgres', 'psql', '-U', 'dev', '-d', 'spralingua_dev', '-c', 
         "SELECT id, email, progress_level, created_at FROM users ORDER BY id;"],
        capture_output=True,
        text=True
    )
    
    print("\nAll users in database:")
    print(result.stdout)
    
    print("\nDatabase test completed successfully!")

if __name__ == '__main__':
    test_docker_database()