








import json
import deck_data

def generate_phygital_payloads():
    phygital_registry = {}
    print("=== MENGHASILKAN PAYLOAD PHYGITAL NFC/QR UNTUK KARTU FISIK ===")
    
    for card in deck_data.starter_deck_database:
        card_id = card['card_id']
        # Format payload aman yang mengarahkan QR/NFC ke hub verifikasi Al-Haqq
        payload = {
            "id": card_id,
            "name": card['name'],
            "category": card['category'],
            "verification_hash": f"ALHAQQ-VERIFIED-{card_id}-2026",
            "digital_sync_url": f"http://localhost:8080/card/{card_id.lower()}"
        }
        phygital_registry[card_id] = payload

    # Simpan ke file JSON terpisah untuk diintegrasikan dengan alat cetak QR
    with open("phygital_payloads.json", "w", encoding="utf-8") as f:
        json.dump(phygital_registry, f, indent=4, ensure_ascii=False)
    
    print(f"Berhasil menghasilkan {len(phygital_registry)} payload phygital ke dalam 'phygital_payloads.json'.")

if __name__ == "__main__":
    generate_phygital_payloads()

