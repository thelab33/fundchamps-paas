from flask import Blueprint, jsonify, abort
from app.models import Example, Sponsor, CampaignGoal, db  
from sqlalchemy import func

api_bp = Blueprint("api", __name__)





@api_bp.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "API live",
        "version": "1.0.0",
        "docs": "/api/docs",  
    })





@api_bp.route("/stats")
def stats():
    
    raised = db.session.query(func.sum(Sponsor.amount)).filter_by(deleted=False, status='approved').scalar() or 0
    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = goal_row.amount if goal_row else 10000
    return jsonify({
        "raised": raised,
        "goal": goal,
        "leaderboard": [
            
            {"name": s.name, "amount": s.amount}
            for s in Sponsor.query.filter_by(deleted=False, status='approved').order_by(Sponsor.amount.desc()).limit(10)
        ]
    })





@api_bp.route("/example/<uuid>", methods=["GET"])
def get_example(uuid):
    ex = Example.by_uuid(uuid)
    if not ex or ex.deleted:
        abort(404, description="Not found or deleted")
    return jsonify(ex.as_dict())

@api_bp.route("/example/<uuid>/delete", methods=["POST"])
def example_soft_delete(uuid):
    ex = Example.by_uuid(uuid)
    if not ex or ex.deleted:
        abort(404, description="Not found or already deleted")
    ex.soft_delete()
    return jsonify({"message": f"{ex.name} soft-deleted."})

@api_bp.route("/example/<uuid>/restore", methods=["POST"])
def example_restore(uuid):
    ex = Example.by_uuid(uuid)
    if not ex or not ex.deleted:
        abort(404, description="Not found or not deleted")
    ex.restore()
    return jsonify({"message": f"{ex.name} restored."})





@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404

@api_bp.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e)}), 400

@api_bp.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Server error", "details": str(e)}), 500








