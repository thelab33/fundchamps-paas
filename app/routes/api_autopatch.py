from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Example, Sponsor, Transaction, CampaignGoal  

def register_model_api(bp, model, name=None):
    model_name = name or model.__tablename__

    
    @bp.route(f"/{model_name}", methods=["GET"])
    def list_items():
        items = model.query.filter_by(deleted=False).all() if hasattr(model, "deleted") else model.query.all()
        return jsonify([item.as_dict() for item in items])

    
    @bp.route(f"/{model_name}/<uuid>", methods=["GET"])
    def get_item(uuid):
        item = model.query.filter_by(uuid=uuid).first()
        if not item or (hasattr(item, "deleted") and item.deleted):
            abort(404, description=f"{model_name.capitalize()} not found or deleted")
        return jsonify(item.as_dict())

    
    @bp.route(f"/{model_name}", methods=["POST"])
    def create_item():
        data = request.get_json() or {}
        item = model(**{k: v for k, v in data.items() if k in model.__table__.columns.keys()})
        db.session.add(item)
        db.session.commit()
        return jsonify(item.as_dict()), 201

    
    @bp.route(f"/{model_name}/<uuid>", methods=["PUT", "PATCH"])
    def update_item(uuid):
        item = model.query.filter_by(uuid=uuid).first()
        if not item or (hasattr(item, "deleted") and item.deleted):
            abort(404, description=f"{model_name.capitalize()} not found or deleted")
        data = request.get_json() or {}
        for k, v in data.items():
            if k in model.__table__.columns.keys():
                setattr(item, k, v)
        db.session.commit()
        return jsonify(item.as_dict())

    
    @bp.route(f"/{model_name}/<uuid>/delete", methods=["POST"])
    def soft_delete_item(uuid):
        item = model.query.filter_by(uuid=uuid).first()
        if not item or (hasattr(item, "deleted") and item.deleted):
            abort(404, description=f"{model_name.capitalize()} not found or already deleted")
        if hasattr(item, "soft_delete"):
            item.soft_delete()
        else:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"{model_name.capitalize()} hard-deleted."})
        return jsonify({"message": f"{model_name.capitalize()} soft-deleted."})

    
    @bp.route(f"/{model_name}/<uuid>/restore", methods=["POST"])
    def restore_item(uuid):
        item = model.query.filter_by(uuid=uuid).first()
        if not item or not (hasattr(item, "deleted") and item.deleted):
            abort(404, description=f"{model_name.capitalize()} not found or not deleted")
        if hasattr(item, "restore"):
            item.restore()
            return jsonify({"message": f"{model_name.capitalize()} restored."})
        abort(400, description="Model does not support restore.")


api_autopatch = Blueprint("api_autopatch", __name__, url_prefix="/api")

@api_autopatch.route("/status")
def status():
    return jsonify({"status": "ok", "message": "Starforge API autopatch live"})


register_model_api(api_autopatch, Example)
register_model_api(api_autopatch, Sponsor)
register_model_api(api_autopatch, Transaction)
register_model_api(api_autopatch, CampaignGoal)




