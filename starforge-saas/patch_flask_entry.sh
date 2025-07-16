#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Patching run.py imports…"
# replace relative import with absolute
sed -i "s|from \\.extensions|from app.extensions|" run.py

echo "📄 Creating manage.py for Flask-CLI…"
cat > manage.py << 'EOF'
#!/usr/bin/env python
# manage.py — entry point for flask run

from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=app.config["DEBUG"]
    )
EOF
chmod +x manage.py

echo "✅ Done!"
echo ""
echo "Next steps:"
echo "  export FLASK_APP=manage.py"
echo "  export FLASK_ENV=development"
echo "  flask run --reload --port 5000"
