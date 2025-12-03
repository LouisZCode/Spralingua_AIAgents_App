"""
Core routes blueprint.
Handles main application routes like landing page.
"""

from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime


core_bp = Blueprint('core', __name__)


@core_bp.route('/')
def landing():
    """Landing page route."""
    if session.get('authenticated'):
        return redirect(url_for('auth.dashboard'))
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return render_template('landing.html', timestamp=timestamp)
