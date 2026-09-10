import json
from datetime import datetime

class KopdesRedemptionEngine:
    def __init__(self, conversion_rate=1.0, max_steps_per_user=10000):
        self.conversion_rate = conversion_rate
        self.max_steps_per_user = max_steps_per_user
        self.min_partner_share = 0.15  # Batas minimum negosiasi 15%
        
        # Aturan Khusus Sembako Kopdes
        self.kopdes_rice_price = 30000  # Harga khusus supplier beras Kopdes per 3kg
        self.max_redemption_cap = 35000  # Batas maksimal nilai item per transaksi
        
        # Database simulasi NIK e-KTP & riwayat klaim
        self.user_database = {}

    def verify_nik_ktp(self, nik: str, full_name: str) -> bool:
        if len(nik) != 16 or not nik.isdigit():
            return False
        if nik not in self.user_database:
            self.user_database[nik] = {
                "name": full_name,
                "claim_count": 0
            }
        return True

    def process_kopdes_redemption(self, nik: str, full_name: str, raw_steps: int, item_choice: str, item_price: int, negotiated_partner_share: float = 0.25) -> dict:
        # 1. Validasi e-KTP
        if not self.verify_nik_ktp(nik, full_name):
            return {"status": "REJECTED", "reason": "Verifikasi e-KTP gagal. NIK harus 16 digit angka valid."}

        # 2. Cek Batas Kuota Maksimal 3x Klaim
        current_claims = self.user_database[nik]["claim_count"]
        if current_claims >= 3:
            return {"status": "REJECTED", "reason": "Batas maksimum klaim (3x) untuk NIK ini telah tercapai."}

        # 3. Validasi Batas Harga Maksimum Item (Maks Rp35.000)
        if item_price > self.max_redemption_cap:
            return {
                "status": "REJECTED", 
                "reason": f"Harga item (Rp{item_price:,}) melebihi batas maksimal klaim Rp{self.max_redemption_cap:,} per transaksi."
            }

        # 4. Validasi 1 Item per Transaksi & Spesifikasi Beras Kopdes jika dipilih
        if "beras" in item_choice.lower() and item_price != self.kopdes_rice_price:
            # Otomatis sesuaikan ke harga khusus Kopdes jika memesan beras kerja sama
            item_price = self.kopdes_rice_price

        # Perhitungan Nilai & Pendanaan (Min Partner 15%)
        partner_share = max(negotiated_partner_share, self.min_partner_share)
        merchant_share = 0.15
        csr_share = 1.0 - (partner_share + merchant_share)

        valid_steps = min(raw_steps, self.max_steps_per_user)
        total_claim_idr = min(valid_steps * self.conversion_rate, item_price)

        amount_partner = total_claim_idr * partner_share
        amount_csr = total_claim_idr * csr_share
        amount_merchant = total_claim_idr * merchant_share

        # Increment riwayat klaim warga
        self.user_database[nik]["claim_count"] += 1
        remaining_quota = 3 - self.user_database[nik]["claim_count"]

        transaction_receipt = {
            "campaign": "September Sehat Grassroots Pilot 2026 (Kopdes Sembako)",
            "timestamp": datetime.now().isoformat(),
            "participant": full_name,
            "nik_masked": nik[:6] + "xxxxxx" + nik[12:],
            "claim_attempt": self.user_database[nik]["claim_count"],
            "remaining_quota": remaining_quota,
            "item_redeemed": item_choice,
            "item_price_idr": item_price,
            "verified_steps_converted": total_claim_idr,
            "penyandang_dana": {
                "partner_share": amount_partner,
                "csr_central_pool": amount_csr,
                "merchant_adjustment": amount_merchant
            },
            "status_code": "SUCCESS_KOPDES_RICE_QRIS",
            "watermark_sig": "AL-HAQQ-PROTOCOL-ICAM"
        }

        return transaction_receipt

if __name__ == "__main__":
    engine = KopdesRedemptionEngine()

    nik_warga = "3171234567890001"
    nama_warga = "Siti Aminah"

    print("--- SIMULASI KLAIM BERAS KOPDES 3KG ---")
    res = engine.process_kopdes_redemption(
        nik_warga, 
        nama_warga, 
        raw_steps=9000, 
        item_choice="Beras Kopdes Khusus 3Kg", 
        item_price=30000, 
        negotiated_partner_share=0.20
    )
    print(json.dumps(res, indent=4))
