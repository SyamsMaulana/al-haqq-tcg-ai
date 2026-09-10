import json
from datetime import datetime

class SecureRedemptionEngine:
    def __init__(self, conversion_rate=1.0, max_steps_per_user=10000):
        self.conversion_rate = conversion_rate
        self.max_steps_per_user = max_steps_per_user
        self.min_partner_share = 0.15  # Batas minimum negosiasi 15%
        
        # Database simulasi penyimpanan data warga (NIK e-KTP & riwayat klaim)
        # Format: { "NIK": {"name": str, "claim_count": int} }
        self.user_database = {}

    def verify_nik_ktp(self, nik: str, full_name: str) -> bool:
        """
        Simulasi verifikasi e-KTP elektronik (panjang NIK harus 16 digit).
        """
        if len(nik) != 16 or not nik.isdigit():
            return False
        
        # Jika NIK baru, daftarkan ke database lokal dengan klaim awal 0
        if nik not in self.user_database:
            self.user_database[nik] = {
                "name": full_name,
                "claim_count": 0
            }
        return True

    def process_secure_redemption(self, nik: str, full_name: str, raw_steps: int, merchant_name: str, negotiated_partner_share: float = 0.25) -> dict:
        """
        Memproses redeem dengan validasi e-KTP dan batas maksimal 3 kali klaim.
        """
        # 1. Validasi e-KTP
        if not self.verify_nik_ktp(nik, full_name):
            return {
                "status": "REJECTED",
                "reason": "Verifikasi e-KTP gagal. NIK harus 16 digit angka yang valid."
            }

        # 2. Cek Batas Kuota Klaim (Maksimal 3x)
        current_claims = self.user_database[nik]["claim_count"]
        if current_claims >= 3:
            return {
                "status": "REJECTED",
                "reason": "Batas maksimum klaim (3x / 3 item) untuk NIK ini telah tercapai. Mencegah monopoli."
            }

        # 3. Validasi Negosiasi Partner (Min 15%)
        partner_share = max(negotiated_partner_share, self.min_partner_share)
        merchant_share = 0.15
        csr_share = 1.0 - (partner_share + merchant_share)

        valid_steps = min(raw_steps, self.max_steps_per_user)
        total_claim_idr = valid_steps * self.conversion_rate

        amount_partner = total_claim_idr * partner_share
        amount_csr = total_claim_idr * csr_share
        amount_merchant = total_claim_idr * merchant_share

        # Increment jumlah klaim pengguna
        self.user_database[nik]["claim_count"] += 1
        remaining_quota = 3 - self.user_database[nik]["claim_count"]

        # Buat Struk Transaksi Sukses
        transaction_receipt = {
            "campaign": "September Sehat Grassroots Pilot 2026",
            "timestamp": datetime.now().isoformat(),
            "participant": full_name,
            "nik_masked": nik[:6] + "xxxxxx" + nik[12:], # Masking NIK untuk privasi
            "claim_attempt": self.user_database[nik]["claim_count"],
            "remaining_quota": remaining_quota,
            "verified_steps": valid_steps,
            "nominal_belanja_total": total_claim_idr,
            "penyandang_dana": {
                "partner_share": amount_partner,
                "csr_central_pool": amount_csr,
                "merchant_adjustment": amount_merchant
            },
            "merchant_partner": merchant_name,
            "status_code": "SUCCESS_SECURED_QRIS",
            "watermark_sig": "AL-HAQQ-PROTOCOL-ICAM"
        }

        return transaction_receipt

if __name__ == "__main__":
    engine = SecureRedemptionEngine()

    # Contoh Simulasi Warga melakukan klaim pertama kali dengan e-KTP valid
    nik_warga = "3171234567890001"
    nama_warga = "Siti Aminah"

    print("--- SIMULASI KLAIM 1 ---")
    res1 = engine.process_secure_redemption(nik_warga, nama_warga, 8000, "Warteg Barokah", 0.20)
    print(json.dumps(res1, indent=4))

    print("\n--- SIMULASI KLAIM KEDUA ---")
    res2 = engine.process_secure_redemption(nik_warga, nama_warga, 7000, "Abang Nasi Goreng Keliling", 0.20)
    print(json.dumps(res2, indent=4))
