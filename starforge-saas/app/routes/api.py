from flask import Blueprint, abort, jsonify, current_app
from sqlalchemy import func

from app.models import CampaignGoal, Example, Sponsor, db

api_bp = Blueprint("api", __name__)

# ─────────────────────────────────────────────────────────────
# 🌐 Health & Fundraising Stats
# ─────────────────────────────────────────────────────────────

@api_bp.route("/status")
def status():
    """Basic API health check."""
    return jsonify({
        "status": "ok",
        "message": "API live",
        "version": "1.0.0",
        "docs": "/api/docs"
    })


@api_bp.route("/stats")
def stats():
    """
    Live fundraising stats and sponsor leaderboard (top 10).
    """
    try:
        # Total raised
        raised = (
            db.session.query(func.sum(Sponsor.amount))
            .filter_by(deleted=False, status="approved")
            .scalar()
            or 0
        )

        # Active goal
        goal_row = CampaignGoal.query.filter_by(active=True).first()
        goal = getattr(goal_row, "goal_amount", 10_000)

        # Leaderboard: top 10 sponsors
        leaderboard = [
            {"name": s.name, "amount": float(s.amount)}
            for s in Sponsor.query
                .filter_by(deleted=False, status="approved")
                .order_by(Sponsor.amount.desc())
                .limit(10)
        ]

        return jsonify({
            "raised": float(raised),
            "goal": float(goal),
            "leaderboard": leaderboard
        })

    except Exception as e:
        current_app.logger.error("Error in /stats: %s", e)
        return jsonify({
            "raised": 0,
            "goal": 10000,
            "leaderboard": [],
            "error": "Database error"
        }), 500


# ─────────────────────────────────────────────────────────────
# 🧪 Example Object (Demo/Docs Purposes)
# ─────────────────────────────────────────────────────────────

@api_bp.route("/example/<uuid>", methods=["GET"])
def get_example(uuid):
    """
    Get a specific Example object by UUID.
    """
    ex = Example.by_uuid(uuid)
    if not ex or ex.deleted:
        abort(404, description="Example not found or deleted")
    return jsonify(ex.as_dict())


@api_bp.route("/example/<uuid>/delete", methods=["POST"])
def example_soft_delete(uuid):
    """
    Soft-delete Example object by UUID.
    """
    ex = Example.by_uuid(uuid)
    if not ex or ex.deleted:
        abort(404, description="Example not found or already deleted")

    ex.soft_delete()
    return jsonify({"message": f"{ex.name} soft-deleted"})


@api_bp.route("/example/<uuid>/restore", methods=["POST"])
def example_restore(uuid):
    """
    Restore a previously soft-deleted Example object.
    """
    ex = Example.by_uuid(uuid)
    if not ex or not ex.deleted:
        abort(404, description="Example not found or not deleted")

    ex.restore()
    return jsonify({"message": f"{ex.name} restored"})


# ─────────────────────────────────────────────────────────────
# ❌ Unified Error Handlers
# ─────────────────────────────────────────────────────────────

@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404


@api_bp.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e)}), 400


@api_bp.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Server error", "details": str(e)}), 500

