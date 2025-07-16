#!/bin/bash
set -e

echo "🛠️ Patching 404 handler and config imports..."

INIT_FILE="app/__init__.py"
RUN_FILE="run.py"

# Check if 404 handler exists first
if grep -q "def page_not_found" "$INIT_FILE"; then
  echo "404 handler already present in $INIT_FILE"
else
  echo "Adding 404 handler to $INIT_FILE..."

  # Insert the 404 handler function before the line containing 'return app' in create_app()
  awk '
    /def create_app.*\(/ {in_func=1}
    in_func && /return app/ {
      print "    @app.errorhandler(404)"
      print "    def page_not_found(e):"
      print "        app.logger.warning(f\"404 Not Found: {request.method} {request.path}\")"
      print "        return (\"<h1>404 Not Found</h1><p>The requested URL was not found on the server.</p>\", 404)"
      in_func=0
    }
    {print}
  ' "$INIT_FILE" > "$INIT_FILE.tmp" && mv "$INIT_FILE.tmp" "$INIT_FILE"
fi

# Fix config import path in run.py
if grep -q "app.app.config" "$RUN_FILE"; then
  echo "Fixing config import paths in $RUN_FILE..."
  sed -i 's/app\.app\.config/app.config/g' "$RUN_FILE"
else
  echo "No config path fix needed in $RUN_FILE"
fi

echo "✅ Patch complete! Restart your Flask server and test 404 logging."
