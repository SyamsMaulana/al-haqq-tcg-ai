


import json
from datetime import datetime
import qrcode

def generate_living_barcode():
    # Payload JSON terstruktur dengan cap digital kolaborasi autentik
    payload = {
        "creator": "Syams Maulana (ICAM)",
        "protocol": "Al-Haqq Protocol",
        "timestamp": datetime.now().isoformat(),
        "status": "Authentic Co-Creation & Digital Stamp",
        "integrity_verification": "Haqq Concept Verified"
    }
    
    # Konversi payload ke string JSON
    json_data = json.dumps(payload, indent=4)
    print("--- Payload JSON Living Barcode ---")
    print(json_data)
    
    # Pembuatan QR Barcode dinamis
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"living_barcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(filename)
    print(f"\nBarcode berhasil disimpan sebagai: {filename}")

if __name__ == "__main__":
    generate_living_barcode()

