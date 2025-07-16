from flask import Blueprint
from flask_restx import Api
from .spotlight import api as spotlight_api
# from .stats import api as stats_api  # Commented out until stats.py exists

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    api_bp,
    version="1.0",
    title="Connect ATX Elite API",
    description="RESTful API for Connect ATX Elite SaaS platform",
    doc="/docs"
)

api.add_namespace(spotlight_api)
# api.add_namespace(stats_api)  # Commented out until stats.py exists


def register_error_handlers(app):
    from flask import jsonify

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

