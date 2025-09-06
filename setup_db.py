import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

# First connect as dev user to postgres database to create the new database
try:
    # Connect to default postgres database first
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="dev",
        password="devpass"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'spralingua_dev'")
    exists = cursor.fetchone()
    
    if exists:
        print("Database 'spralingua_dev' already exists. Dropping it...")
        # Terminate existing connections
        cursor.execute("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = 'spralingua_dev' AND pid <> pg_backend_pid()
        """)
        cursor.execute("DROP DATABASE spralingua_dev")
        print("Database dropped.")
    
    # Create the database
    cursor.execute("CREATE DATABASE spralingua_dev")
    print("Database 'spralingua_dev' created successfully!")
    
    cursor.close()
    conn.close()
    
    # Now connect to the new database to create tables
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="spralingua_dev",
        user="dev",
        password="devpass"
    )
    cursor = conn.cursor()
    
    # Create users table with simplified schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            progress_level INTEGER DEFAULT 0 NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create an index on email for faster lookups
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    
    conn.commit()
    print("Table 'users' created successfully!")
    
    # Test the connection
    cursor.execute("SELECT current_database(), current_user")
    db_info = cursor.fetchone()
    print(f"Connected to database: {db_info[0]} as user: {db_info[1]}")
    
    # Show table structure
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default 
        FROM information_schema.columns 
        WHERE table_name = 'users'
        ORDER BY ordinal_position
    """)
    
    print("\nTable structure:")
    print("-" * 60)
    for row in cursor.fetchall():
        print(f"{row[0]:20} {row[1]:15} NULL:{row[2]:5} Default:{row[3]}")
    
    cursor.close()
    conn.close()
    print("\nDatabase setup completed successfully!")
    
except psycopg2.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")