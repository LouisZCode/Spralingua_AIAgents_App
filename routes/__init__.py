"""
Routes module - Flask Blueprints for route organization.
"""

from .core import core_bp
from .auth import auth_bp
from .exercises import exercises_bp
from .api import api_bp

__all__ = ['core_bp', 'auth_bp', 'exercises_bp', 'api_bp']


def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
