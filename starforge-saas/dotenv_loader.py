import os
from dotenv import load_dotenv, find_dotenv

def init_env():
    env_file = find_dotenv()
    if env_file:
        load_dotenv(env_file)
        print(f"✅ Loaded .env from: {env_file}")
    else:
        print("⚠️ No .env file found.")

# Call init_env() early in manage.py or app/__init__.py
