










# phygital_payload_generator.py — Generator Payload Kriptografis untuk Verifikasi Phygital Kartu TCG
import json
import hashlib
import deck_data
import agent_data

def generate_payloads():
    payloads = {}
    
    # Proses Basis Data Kartu Starter
    for card in deck_data.starter_deck_database:
        card_id = card["card_id"]
        raw_string = f"ALHAQQ-TCG-{card_id}-{card['name']}-2026"
        verification_hash = hashlib.sha256(raw_string.encode()).hexdigest()[:16].upper()
        payloads[card_id] = {
            "card_id": card_id,
            "name": card["name"],
            "type": "Starter Deck",
            "verification_hash": f"ALHAQQ-VERIFIED-{verification_hash}",
            "timestamp": "2026-09-14"
        }

    # Proses Basis Data Karsa Agents
    for agent in agent_data.karsa_agents_database:
        agent_id = agent["agent_id"]
        raw_string = f"ALHAQQ-TCG-{agent_id}-{agent['name']}-2026"
        verification_hash = hashlib.sha256(raw_string.encode()).hexdigest()[:16].upper()
        payloads[agent_id] = {
            "card_id": agent_id,
            "name": agent["name"],
            "type": "Karsa Agent",
            "verification_hash": f"ALHAQQ-VERIFIED-{verification_hash}",
            "timestamp": "2026-09-14"
        }

    with open("phygital_payloads.json", "w", encoding="utf-8") as f:
        json.dump(payloads, f, indent=4)
    
    print(f"Berhasil meng-generate {len(payloads)} payload verifikasi phygital ke 'phygital_payloads.json'.")

if __name__ == "__main__":
    generate_payloads()

