import json
import os

CONFIG_FILE = 'config.json'

def get_mode():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f).get('mode', 'enjoyer')
    return 'enjoyer'

def set_mode(mode):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"mode": mode}, f)
