# Connect ATX Elite

Production-ready Flask app for Connect ATX Elite, featuring:
- Modular app factory pattern
- SQLAlchemy ORM & migrations
- Flask-SocketIO for realtime
- TailwindCSS & modular partials
- Clean blueprints for API, SMS, and more

## Quickstart

1. Install requirements  
   `pip install -r requirements.txt`

2. Run migrations  
   `flask db init && flask db migrate -m "init" && flask db upgrade`

3. Run server  
   `python run.py`

4. For SocketIO in prod, use:  
   `gunicorn -k eventlet -w 1 run:app`

---

## Folder Structure

See `/app` for all source code, `/migrations` for Alembic migrations, `/tests` for pytest unit tests.

---

*Happy Hacking!* 🚀
