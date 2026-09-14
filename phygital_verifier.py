






# phygital_verifier.py — Modul Verifikasi Real-Time Phygital NFC/QR Card
import json
import os

class PhygitalVerifier:
    def __init__(self, payload_path="phygital_payloads.json"):
        self.payload_path = payload_path
        self.payloads = self.load_payloads()

    def load_payloads(self):
        if os.path.exists(self.payload_path):
            with open(self.payload_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def verify_token(self, verification_hash):
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

if __name__ == "__main__":
    verifier = PhygitalVerifier()
    test_hash = "ALHAQQ-VERIFIED-AH-001-2026"
    result = verifier.verify_token(test_hash)
    print(f"Hasil Verifikasi Phygital: {result}")
