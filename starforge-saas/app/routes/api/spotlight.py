from flask_restx import Namespace, Resource
from app.models.sponsor import Sponsor

api = Namespace("spotlight", description="Sponsor spotlight related operations")

@api.route("/")
class SpotlightSponsor(Resource):
    def get(self):
        """
        Returns the latest sponsor info with VIP status.

        VIP is defined as amount >= $100.
        """
        sponsor = Sponsor.query.order_by(Sponsor.created_at.desc()).first()
        if sponsor:
            response = {
                "name": sponsor.name,
                "is_vip": sponsor.amount >= 100,
                "amount": float(sponsor.amount),
            }
            return response, 200
        return {}, 204

