







# phygital_verifier.py — Modul Verifikasi & Aset Fisik Al-Haqq Protocol TCG
import json
import os
import hashlib

class PhygitalVerifier:
    def __init__(self, payload_path="phygital_payloads.json"):
        self.payload_path = payload_path
        self.payloads = self.load_payloads()

    def load_payloads(self):
        if os.path.exists(self.payload_path):
            with open(self.payload_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def generate_card_hash(self, card_id: str, owner: str) -> str:
        payload = f"{card_id}:{owner}:AL_HAQQ_PROTOCOL_2026"
        return hashlib.sha256(payload.encode()).hexdigest()

    def verify_token(self, verification_hash: str):
        for card_id, data in self.payloads.items():
            if data.get("verification_hash") == verification_hash:
                return {
                    "status": "AUTENTIK",
                    "card_id": card_id,
                    "timestamp": data.get("timestamp"),
                    "framework": "Al-Haqq-Protocol v1.0"
                }
        return {
            "status": "TIDAK VALID / ANOMALI",
            "card_id": None,
            "timestamp": None,
            "framework": "Al-Haqq-Protocol v1.0"
        }

    def render_printable_asset(self, card_name: str, card_id: str, owner: str):
        h = self.generate_card_hash(card_id, owner)
        html_template = f"""
        <div style="width: 63mm; height: 88mm; border: 2px solid #000; padding: 4mm; box-sizing: border-box; font-family: sans-serif; position: relative; background: white;">
            <h3>{card_name}</h3>
            <p><b>ID:</b> {card_id}</p>
            <p><b>Owner:</b> {owner}</p>
            <div style="position: absolute; bottom: 4mm; font-size: 8px; word-break: break-all;">
                <b>SHA-256 Hash:</b><br>{h}
            </div>
        </div>
        """
        return html_template

if __name__ == "__main__":
    verifier = PhygitalVerifier()
    print("Modul Phygital Verifier & Asset Exporter siap diintegrasikan.")

