# 1. Set up reports folder
mkdir -p reports && \

# 2. Python & Security Audit (auto-fix lint + security scan)
ruff check . --fix && bandit -r app -ll -q > reports/python_security.txt && \

# 3. Dependency Vulnerability Check
pip install -q safety && safety check -r requirements.txt --full-report > reports/pip_vulns.txt && \

# 4. HTML Template & Jinja2 Lint (find common template errors)
pip install -q jinja2-cli jinja2-lint && \
find app/templates -name '*.html' | xargs jinja2-lint > reports/jinja2_lint.txt 2>&1 && \

# 5. Static Asset Audit (broken CSS/JS/img references)
grep -RhoP "static/[^\s\"')>]+" app/templates | sort -u | \
while read -r asset; do [ -f "app/static/${asset#static/}" ] || echo "$asset"; done > reports/missing_static_assets.txt && \

# 6. CSS Lint/Compile Errors (Tailwind + others)
npx tailwindcss -i app/static/css/tailwind.src.css -o app/static/css/tailwind.min.css --minify 2> reports/tailwind_errors.txt && \
npx stylelint "**/*.css" > reports/css_lint.txt 2>&1 || true && \

# 7. JS Audit (quick scan for obvious bugs)
npx eslint app/static/js/*.js > reports/js_lint.txt 2>&1 || true && \

# 8. Flask Route + Import Checker (broken views)
grep -R "url_for(" app/templates | sed -E "s/.*url_for\(['\"]([^'\"]+)['\"].*/\1/" | sort -u | \
while read route; do grep -q "def $route" app/routes/*.py || echo "$route"; done > reports/missing_flask_routes.txt && \

# 9. Database Migration Health
flask db migrate -m "check" && flask db upgrade && echo "OK" > reports/db_status.txt || echo "ERROR" > reports/db_status.txt && \

# 10. Mini UX Screenshot (optional, for pro: needs Google Chrome)
which google-chrome && google-chrome --headless --screenshot --window-size=1280,800 http://localhost:5000 > /dev/null 2>&1 && mv screenshot.png reports/ux_snapshot.png || echo "skip screenshot"
