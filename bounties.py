import json
import os

BOUNTY_FILE = 'bounties_log.json'

def load_bounties():
    if os.path.exists(BOUNTY_FILE):
        with open(BOUNTY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_bounty(player_name, bounty_title, description):
    bounties = load_bounties()
    bounties.append({
        "player": player_name,
        "title": bounty_title,
        "description": description
    })
    with open(BOUNTY_FILE, 'w') as f:
        json.dump(bounties, f, indent=4)
