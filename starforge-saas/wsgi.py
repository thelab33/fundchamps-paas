"""WSGI entry point for any server or cloud."""
from app import create_app

# You can set env vars before deploy (FLASK_ENV, FLASK_CONFIG, etc.)
app = create_app()

# Optionally, run locally for testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
