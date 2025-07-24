from flask import current_app
from app.models import User

# Import necessary components at the top to avoid circular imports
from flask_login import current_user
from app.extensions import login_manager


# --- User Loader ---
@login_manager.user_loader
def load_user(user_id):
    """Loads the user by their ID."""
    return User.query.get(int(user_id))


# --- Context Processor for User ---
@current_app.context_processor
def inject_user():
    """Inject the current user into the template context."""
    return dict(current_user=current_user)
