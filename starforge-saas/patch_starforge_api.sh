#!/bin/bash

set -e
echo "🔧 Starforge API Patch — Initiated..."

# Timestamped backups
ts=$(date +%s)
mkdir -p backups
for f in app/api.py app/__init__.py; do
    cp "$f" "backups/$(basename "$f").bak.$ts"
done

# 1. Patch __init__.py to register api_bp
echo "✅ Ensuring Blueprint is registered..."
grep -q "api_bp" app/__init__.py || sed -i "/def create_app/i\\
from app.api import api_bp" app/__init__.py
grep -q "register_blueprint(api_bp)" app/__init__.py || sed -i "/app.config.from_object/a\\
    app.register_blueprint(api_bp)" app/__init__.py

# 2. Add app/api/models.py if missing
echo "📦 Creating Swagger models module..."
mkdir -p app/api
cat > app/api/models.py <<EOF
from flask_restx import fields

def register_models(api):
    stats_model = api.model('Stats', {
        'raised': fields.Float(description='Total raised', example=5000.0),
        'goal': fields.Float(description='Goal', example=10000.0),
        'leaderboard': fields.List(fields.Nested(api.model('Leaderboard', {
            'name': fields.String(example='Sponsor'),
            'amount': fields.Float(example=500)
        })))
    })

    status_model = api.model('Status', {
        'status': fields.String(example='ok'),
        'message': fields.String(example='API live'),
        'version': fields.String(example='1.0.0'),
        'docs': fields.String(example='/api/docs')
    })

    return {"stats": stats_model, "status": status_model}
EOF

# 3. Patch CORS support into __init__.py
echo "🌍 Enabling CORS for API..."
grep -q "CORS(app)" app/__init__.py || sed -i "/Flask(__name__)/a\\
    from flask_cors import CORS\n    CORS(app)" app/__init__.py

# 4. Append /example list and POST endpoint
echo "📬 Adding /example route (list + post)..."
cat >> app/api.py <<'EOF'

@api.route('/example')
class ExampleList(Resource):
    def get(self):
        """
        List all examples.
        """
        examples = Example.query.filter_by(deleted=False).all()
        return jsonify([e.as_dict() for e in examples])

    def post(self):
        """
        Create a new example (expects JSON: { "name": ... })
        """
        from flask import request
        data = request.get_json()
        if not data or "name" not in data:
            abort(400, description="Missing 'name' in request body")

        new_example = Example(name=data["name"])
        db.session.add(new_example)
        db.session.commit()
        return jsonify(new_example.as_dict()), 201
EOF

# 5. Improve /stats fallback logging
echo "🧠 Enhancing fallback logic in /stats..."
sed -i '/goal = getattr(goal_row, "goal_amount", 10_000)/c\
goal = getattr(goal_row, "goal_amount", None)\n            if goal is None:\n                current_app.logger.warning("⚠️ No active CampaignGoal found — using fallback.")\n                goal = 10000' app/api.py

# 6. Stub Bearer-protected route
echo "🔐 Adding stub for protected Bearer route..."
cat >> app/api.py <<'EOF'

@api.route('/private')
class PrivateResource(Resource):
    @api.doc(security='Bearer')
    def get(self):
        abort(401, description="🔒 Protected route — implement auth")
EOF

# 7. Inject authorizations in API init
sed -i "/Api(api_bp, version=/i\
authorizations = {\n    'Bearer': {\n        'type': 'apiKey',\n        'in': 'header',\n        'name': 'Authorization'\n    }\n}" app/api.py

sed -i "/Api(api_bp, version=/c\
api = Api(api_bp, version='1.0', title='Connect ATX Elite API', description='API for the Connect ATX Elite platform', doc='/docs', authorizations=authorizations)"

echo "🎯 Installing flask-cors if not installed..."
pip install flask-cors > /dev/null

echo "✅ Starforge API Patch Complete!"
