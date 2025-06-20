import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
token_blacklist = []

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)