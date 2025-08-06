#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Starforge Auto Patch: applies safe, idempotent upgrades to:
#  - app/__init__.py
#  - app/templates/base.html
# Creates timestamped backups under .patch_backups/YYYYmmdd-HHMMSS/
# Flags:
#   --dry-run     : show diffs, do not write
#   --only-init   : patch only app/__init__.py
#   --only-base   : patch only app/templates/base.html
#   --no-build    : skip npm/css checks
#   --no-git      : skip git commit
# ─────────────────────────────────────────────────────────────────────────────

DRY_RUN=false
ONLY_INIT=false
ONLY_BASE=false
NO_BUILD=false
NO_GIT=false

for arg in "${@:-}"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --only-init) ONLY_INIT=true ;;
    --only-base) ONLY_BASE=true ;;
    --no-build) NO_BUILD=true ;;
    --no-git) NO_GIT=true ;;
    *) echo "Unknown flag: $arg" >&2; exit 1 ;;
  esac
done

ROOT="$(pwd)"
timestamp() { date +"%Y%m%d-%H%M%S"; }
TS="$(timestamp)"
BACKUP_DIR="$ROOT/.patch_backups/$TS"
mkdir -p "$BACKUP_DIR"

require_path() {
  local p="$1"
  [[ -e "$p" ]] || { echo "❌ Missing: $p" >&2; exit 1; }
}

# Validate expected structure
require_path "app"
require_path "app/__init__.py"
mkdir -p "app/templates"
require_path "app/templates"
mkdir -p "app/templates/partials"
mkdir -p "app/static/css" "app/static/js" "app/static/images"

# ── New file contents (heredocs) ─────────────────────────────────────────────

read -r -d '' NEW_INIT_PY <<'PY'
from __future__ import annotations

"""
Starforge Flask application factory.
All routes are registered via Blueprints — see `app/routes`, etc.
"""

from typing import Any, Type, Optional
import logging
import os
from datetime import datetime
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Load environment early
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Core extensions
from app.extensions import db, migrate, socketio, mail  # noqa: E402

# Optional extensions (Flask-Login, Babel, CLI)
USE_LOGIN = USE_BABEL = USE_CLI = False

try:
    from flask_login import LoginManager, current_user
    login_manager: Optional[LoginManager] = LoginManager()
    USE_LOGIN = True
except ImportError:
    login_manager = None

try:
    from flask_babel import Babel, _ as _t
    USE_BABEL = True
except ImportError:
    Babel = None  # type: ignore
    _t = lambda s: s

try:
    from app.cli import starforge
    USE_CLI = True
except ImportError:
    starforge = None  # type: ignore


def _resolve_config(dotted_or_class: str | Type[Any]) -> str | Type[Any]:
    """Accept dotted path or class; tolerate the legacy DevelopmentConfig path."""
    if isinstance(dotted_or_class, str):
        candidate = dotted_or_class
        if candidate == "app.config.config.DevelopmentConfig":
            candidate = "app.config.DevelopmentConfig"
        return candidate
    return dotted_or_class


def _json_error(message: str, status: int, **extra: Any):
    return jsonify({"status": "error", "message": message, **extra}), status


def _file_mtime_version(path: Path) -> int:
    try:
        return int(path.stat().st_mtime)
    except Exception:
        return int(datetime.utcnow().timestamp())


def _register_optional_bp(app: Flask, module_path: str, url_prefix: str, attr_candidates=("api_bp", "bp")):
    """Register blueprint if module exists and exposes a bp."""
    if find_spec(module_path) is None:
        logging.info("Skipping blueprint %s (module missing)", module_path)
        return
    try:
        mod = import_module(module_path)
        bp = None
        for attr in attr_candidates:
            bp = getattr(mod, attr, None)
            if bp:
                break
        if not bp:
            logging.info("Skipping blueprint %s (no blueprint attribute found)", module_path)
            return
        app.register_blueprint(bp, url_prefix=url_prefix)
        logging.info("Registered %s at %s", module_path, url_prefix)
    except Exception as exc:
        logging.exception("Failed to register blueprint %s: %s", module_path, exc)


def create_app(config_class: str | Type[Any] | None = None) -> Flask:
    """Create and configure the Starforge Flask app."""
    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / "app/static"),
        template_folder=str(BASE_DIR / "app/templates"),
    )

    # 1) Config
    default_cfg = os.getenv("FLASK_CONFIG", "app.config.DevelopmentConfig")
    target_cfg = _resolve_config(config_class or default_cfg)
    try:
        app.config.from_object(target_cfg)
    except (ImportError, AttributeError, ModuleNotFoundError) as exc:
        legacy = "app.config.config.DevelopmentConfig"
        if isinstance(target_cfg, str) and target_cfg != legacy:
            try:
                app.config.from_object(legacy)
            except Exception:
                raise RuntimeError(f"❌ Invalid FLASK_CONFIG '{target_cfg}': {exc}") from exc
        else:
            raise RuntimeError(f"❌ Invalid FLASK_CONFIG '{target_cfg}': {exc}") from exc

    # 2) Logging
    logging.basicConfig(
        level=app.config.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.getLogger("werkzeug").setLevel(app.config.get("WERKZEUG_LOG_LEVEL", "WARNING"))
    logging.info("Loaded configuration: %s | DEBUG=%s", app.config.get("ENV", "unknown"), app.debug)
    logging.info("DB: %s", app.config.get("SQLALCHEMY_DATABASE_URI", "<unset>"))

    # 3) CORS
    default_origin = "*" if app.config.get("ENV") != "production" else os.getenv("PRIMARY_ORIGIN", "https://connect-atx-elite.com")
    cors_origins = os.getenv("CORS_ORIGINS", default_origin)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": cors_origins}})

    # 4) Security (optional CSP)
    if app.config.get("ENV") == "production":
        try:
            from flask_talisman import Talisman
            Talisman(app, content_security_policy=None)
        except ModuleNotFoundError:
            logging.warning("⚠️ flask-talisman not installed – skipping CSP setup")

    # 5) Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins=cors_origins)
    mail.init_app(app)

    # 6) Request ID
    @app.before_request
    def _assign_request_id():
        g.request_id = request.headers.get("X-Request-ID", uuid4().hex)

    @app.after_request
    def _inject_request_id(resp):
        resp.headers.setdefault("X-Request-ID", getattr(g, "request_id", uuid4().hex))
        return resp

    # 7) Login Manager (optional)
    if USE_LOGIN and login_manager:
        login_manager.init_app(app)
        try:
            from app.models.user import User  # local import
        except Exception as exc:
            logging.warning("Login enabled but User model import failed: %s", exc)
            User = None  # type: ignore

        @login_manager.user_loader
        def load_user(user_id: str):
            if not User:
                return None
            try:
                return User.query.get(int(user_id))
            except Exception:
                return None

        @app.context_processor
        def _inject_user() -> dict[str, Any]:
            return {"current_user": current_user}
    else:
        @app.context_processor
        def _inject_user() -> dict[str, Any]:
            class _Anon:
                is_authenticated = False
                def __bool__(self): return False
            return {"current_user": _Anon()}

    # 8) Babel (optional)
    if USE_BABEL and Babel:
        babel = Babel(app)
        @app.context_processor
        def _inject_babel():
            return {"_": _t}
    else:
        @app.context_processor
        def _inject_noop():
            return {"_": (lambda s: s)}

    # 9) CLI (optional)
    if USE_CLI and starforge:
        app.cli.add_command(starforge)

    # 10) Template context
    @app.context_processor
    def _inject_env() -> dict[str, Any]:
        return {"app_env": app.config.get("ENV"), "app_config": app.config}

    @app.context_processor
    def _inject_now() -> dict[str, Any]:
        return {"now": datetime.utcnow}

    @app.context_processor
    def _inject_team() -> dict[str, Any]:
        class _Empty:
            def __getattr__(self, _): return None
            def __str__(self) -> str: return ""
        return {"team": _Empty()}

    @app.context_processor
    def _inject_asset_versions() -> dict[str, Any]:
        css = Path(app.static_folder or "app/static") / "css" / "tailwind.min.css"
        js = Path(app.static_folder or "app/static") / "js" / "main.js"
        return {"asset_version": max(_file_mtime_version(css), _file_mtime_version(js))}

    # 11) Filters
    def _comma_like(val: Any) -> Any:
        try:
            return f"{int(val):,}"
        except (ValueError, TypeError):
            return val
    app.add_template_filter(_comma_like, "comma")
    app.add_template_filter(_comma_like, "commafy")

    # 12) Errors — JSON for /api or Accept: application/json
    @app.errorhandler(HTTPException)
    def _handle_http_exc(err: HTTPException):
        if "application/json" in request.headers.get("Accept", "") or request.path.startswith("/api"):
            return _json_error(err.description or err.name, err.code or 500)
        return err

    @app.errorhandler(Exception)
    def _handle_uncaught(err: Exception):
        logging.exception("Unhandled error: %s", err)
        if "application/json" in request.headers.get("Accept", "") or request.path.startswith("/api"):
            return _json_error("Internal Server Error", 500, request_id=getattr(g, "request_id", None))
        return err

    # 13) Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    _register_optional_bp(app, "app.api", "/api")
    _register_optional_bp(app, "app.sms", "/sms")

    try:
        admin_bp = import_module("app.admin.routes").admin
        app.register_blueprint(admin_bp, url_prefix="/admin")
        logging.info("Registered admin dashboard at /admin")
    except (ModuleNotFoundError, AttributeError) as exc:
        logging.info("Admin dashboard not found – skipping (%s)", exc)

    # 14) Health & Version
    @app.get("/healthz")
    def _healthz():
        return {"status": "ok", "message": "Starforge Flask live!", "request_id": getattr(g, "request_id", None)}

    @app.get("/version")
    def _version():
        return {"version": os.getenv("GIT_COMMIT", "dev"), "env": app.config.get("ENV")}

    # 15) Banner (once, even with reloader)
    should_print = (not app.debug) or (os.environ.get("WERKZEUG_RUN_MAIN") == "true")
    if should_print:
        print("\n".join((
            "┌────────────────────────────────────────────┐",
            "│  🌟 Starforge SaaS: Flask Ready to Launch  │",
            f"│  ENV = {app.config.get('ENV','unknown'):<12}   DEBUG = {str(app.debug):<5}   │",
            "└────────────────────────────────────────────┘",
        )))

    return app


__all__ = ["create_app"]
PY

read -r -d '' NEW_BASE_HTML <<'HTML'
<!DOCTYPE html>
<html
  lang="{{ lang_code or 'en' }}"
  data-theme="{{ theme or 'dark' }}"
  class="no-js scroll-smooth antialiased bg-zinc-950 text-white font-sans{% if team and team.body_class %} {{ team.body_class }}{% endif %}"
>
<head>
  {# Meta & SEO #}
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
  <meta name="robots" content="index,follow,max-image-preview:large" />
  <meta name="theme-color" content="{{ team.theme_color or '#facc15' }}" />
  <meta name="color-scheme" content="dark light" />
  <link rel="canonical" href="{{ request.url_root|trim('/') }}" />
  <meta name="description" content="{{ team.meta_description or 'Connect ATX Elite — Family-run AAU basketball building future leaders in East Austin.' }}" />

  {# Open Graph & Twitter #}
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{{ team.og_title or 'Connect ATX Elite | Empowering Youth' }}" />
  <meta property="og:description" content="{{ team.og_description or 'Support our basketball journey and invest in our next generation of leaders.' }}" />
  {% set _ogimg = (team and team.og_image) and (team.og_image if team.og_image.startswith('http') else url_for('static', filename=team.og_image)) or url_for('static', filename='images/logo.avif') %}
  <meta property="og:image" content="{{ _ogimg }}" />
  <meta property="og:url" content="{{ request.url }}" />
  <meta property="og:site_name" content="{{ team.team_name or 'Connect ATX Elite' }}" />
  <meta property="og:image:alt" content="{{ team.og_alt or team.og_title or 'Connect ATX Elite' }}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:creator" content="{{ team.twitter_handle or '@ConnectATXElite' }}" />

  <title>{% block title %}{{ team.team_name or 'Connect ATX Elite' }}{% endblock %}</title>

  {# PWA & Icons #}
  <link rel="manifest" href="{{ url_for('static', filename='site.webmanifest', v=asset_version) }}" />
  <link rel="icon" type="image/png" sizes="32x32"
        href="{{ (team.favicon and url_for('static', filename=team.favicon, v=asset_version)) or url_for('static', filename='images/favicon.png', v=asset_version) }}" />
  <link rel="apple-touch-icon"
        href="{{ (team.apple_icon and url_for('static', filename=team.apple_icon, v=asset_version)) or url_for('static', filename='images/logo.avif', v=asset_version) }}" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

  {# Performance hints #}
  <meta http-equiv="x-dns-prefetch-control" content="on" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

  {# Fonts (self-host later for strict CSP) #}
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />

  {# Styles: preload + main CSS (cache-busted) #}
  <link rel="preload" href="{{ url_for('static', filename='css/tailwind.min.css', v=asset_version) }}" as="style" />
  <link rel="stylesheet" href="{{ url_for('static', filename='css/tailwind.min.css', v=asset_version) }}" media="all" />

  {# Dev-only CSS #}
  {% if app_env != 'production' %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/input.css', v=asset_version) }}">
  {% endif %}

  {# Team-specific overrides #}
  {% if team and team.custom_css %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/' ~ team.custom_css, v=asset_version) }}" />
  {% endif %}

  {% block head_extra %}{% endblock %}
</head>

<body class="bg-zinc-950 text-white font-sans antialiased min-h-screen flex flex-col{% if team and team.body_class %} {{ team.body_class }}{% endif %}">
  <script>
    document.documentElement.classList.remove('no-js'); document.documentElement.classList.add('js');
  </script>

  <a href="#main-content"
     class="sr-only focus:not-sr-only absolute top-2 left-2 bg-yellow-400 text-black font-semibold px-3 py-1 rounded-lg z-50"
     tabindex="0">Skip to main content</a>

  {% block announcement %}{% endblock %}
  {% include 'partials/header_and_announcement.html' ignore missing %}

  {% block hero %}{% endblock %}

  <main id="main-content" role="main" tabindex="-1"
        class="min-h-[60vh] flex flex-col gap-14 max-w-6xl w-full mx-auto px-2 sm:px-8 pt-6"
        style="scroll-margin-top: 80px;">
    {% block content %}{% endblock %}
  </main>

  {% include 'partials/footer.html' ignore missing %}

  {% block global_modals %}
    {% include 'partials/newsletter.html' ignore missing %}
  {% endblock %}

  {% block pre_scripts %}{% endblock %}
  <script src="{{ url_for('static', filename='js/main.js', v=asset_version) }}" defer></script>
  {% block scripts %}{% endblock %}
  {% block post_scripts %}{% endblock %}
</body>
</html>
HTML

# ── Helpers ──────────────────────────────────────────────────────────────────

backup_and_write() {
  local target="$1" ; local content="$2"
  local target_dir ; target_dir="$(dirname "$target")"
  mkdir -p "$target_dir"

  # Temp file for comparison
  local tmp ; tmp="$(mktemp)"
  printf "%s" "$content" > "$tmp"

  if [[ -f "$target" ]]; then
    if diff -u "$target" "$tmp" >/dev/null 2>&1; then
      echo "✓ No change for $target"
      rm -f "$tmp"
      return 0
    fi
    mkdir -p "$BACKUP_DIR/$(dirname "$target")"
    cp -a "$target" "$BACKUP_DIR/$target"
    echo "↻ Backed up $target -> $BACKUP_DIR/$target"
  else
    echo "• Creating $target"
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "–– DRY RUN: showing diff for $target ––"
    diff -u "${target:-/dev/null}" "$tmp" || true
    rm -f "$tmp"
  else
    mv "$tmp" "$target"
    echo "✔ Wrote $target"
  fi
}

node_exists() { command -v node >/dev/null 2>&1; }
npm_exists() { command -v npm >/dev/null 2>&1; }

maybe_build_css() {
  [[ "$NO_BUILD" == "true" ]] && { echo "⏭  Skipping CSS build (flag)"; return; }
  if [[ ! -f "app/static/css/tailwind.min.css" ]]; then
    if npm_exists && [[ -f package.json ]]; then
      echo "⚙️  tailwind.min.css missing → running npm run build"
      npm run build || true
    else
      echo "ℹ️  tailwind.min.css missing and npm not available; skipping build"
    fi
  fi
}

python_syntax_check() {
  python3 - <<'PY' || { echo "❌ Python syntax check failed"; exit 1; }
import sys
try:
    from app import create_app
    app = create_app()
    print("OK: create_app() callable")
except Exception as e:
    print("ERR:", e)
    sys.exit(1)
PY
}

git_commit() {
  [[ "$NO_GIT" == "true" ]] && return 0
  if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "⏭  Skipping git commit (dry-run)"
    else
      git add app/__init__.py app/templates/base.html || true
      if ! git diff --cached --quiet; then
        git commit -m "Starforge autopatch: app factory + base.html (asset_version, optional BPs, single banner)"
        echo "✓ Changes committed"
      else
        echo "✓ Nothing to commit"
      fi
    fi
  fi
}

# ── Patch execution ──────────────────────────────────────────────────────────

PATCH_INIT=true
PATCH_BASE=true
$ONLY_INIT && PATCH_BASE=false
$ONLY_BASE && PATCH_INIT=false

$PATCH_INIT && backup_and_write "app/__init__.py" "$NEW_INIT_PY"
$PATCH_BASE && backup_and_write "app/templates/base.html" "$NEW_BASE_HTML"

maybe_build_css
python_syntax_check
git_commit

echo
echo "✅ Autopatch complete."
echo "Backups: $BACKUP_DIR"
$DRY_RUN && echo "Note: DRY RUN made no changes."

