"""
Services module - External API clients and service integrations.
"""

from .claude_client import ClaudeClient
from .minimax_client import MinimaxClient, minimax_client
from .feedback import (
    generate_language_hint,
    generate_comprehensive_feedback,
    get_message_requirement
)

__all__ = [
    'ClaudeClient',
    'MinimaxClient',
    'minimax_client',
    'generate_language_hint',
    'generate_comprehensive_feedback',
    'get_message_requirement'
]
