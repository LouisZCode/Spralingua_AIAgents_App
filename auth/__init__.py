"""
Authentication module for Spralingua.
"""

from .auth_manager import AuthManager
from .decorators import login_required, guest_only
from .forms import LoginForm, RegistrationForm

__all__ = [
    'AuthManager',
    'login_required',
    'guest_only',
    'LoginForm',
    'RegistrationForm'
]
