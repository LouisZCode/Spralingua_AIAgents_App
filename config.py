"""
Application configuration for Spralingua.
Centralizes all configuration in one place.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class."""

    # Flask core
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(32).hex())

    # Database
    _database_url = os.getenv('DATABASE_URL')
    # Fix Railway's postgres:// to postgresql:// for SQLAlchemy
    if _database_url and _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = bool(os.getenv('RAILWAY_ENVIRONMENT'))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # WTForms / CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens

    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    MINIMAX_API_KEY = os.getenv('MINIMAX_API_KEY')
    MINIMAX_GROUP_ID = os.getenv('MINIMAX_GROUP_ID')
    MINIMAX_VOICE_ID = os.getenv('MINIMAX_VOICE_ID', 'female-shaonv')

    # Environment detection
    IS_PRODUCTION = bool(os.getenv('RAILWAY_ENVIRONMENT'))
    DEBUG = not IS_PRODUCTION

    @classmethod
    def log_config(cls):
        """Log configuration status (masked for security)."""
        db_url = cls.SQLALCHEMY_DATABASE_URI
        if db_url:
            masked = db_url[:50] + "..." if len(db_url) > 50 else db_url
            print(f"[CONFIG] Database: {masked}")
        else:
            print("[CONFIG ERROR] No DATABASE_URL found!")

        print(f"[CONFIG] Production mode: {cls.IS_PRODUCTION}")
        print(f"[CONFIG] Anthropic API configured: {bool(cls.ANTHROPIC_API_KEY)}")
        print(f"[CONFIG] Minimax API configured: {bool(cls.MINIMAX_API_KEY)}")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get the appropriate configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
