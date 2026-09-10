import json
from datetime import datetime

class ZeroErrorRedemptionEngine:
    def __init__(self, conversion_rate=1.0, max_steps_per_user=10000):
        self.conversion_rate = float(conversion_rate)
        self.max_steps_per_user = int(max_steps_per_user)
        self.min_partner_share = 0.15
        self.kopdes_rice_price = 30000
        self.max_redemption_cap = 35000
        self.user_database = {}

    def _validate_nik(self, nik: str) -> bool:
        if not isinstance(nik, str) or len(nik) != 16 or not nik.isdigit():
            return False
        return True

    def process_transaction(self, nik: str, full_name: str, raw_steps: int, item_choice: str, item_price: int, negotiated_partner_share: float = 0.20) -> dict:
        cleaned_nik = str(nik).strip()
        cleaned_name = str(full_name).strip()
        
        if not self._validate_nik(cleaned_nik):
            return {
                "status": "REJECTED_ERROR",
                "error_code": "ERR_INVALID_NIK",
                "message": "Validasi e-KTP gagal. NIK wajib berupa 16 digit angka valid."
            }

        if not cleaned_name:
            return {
                "status": "REJECTED_ERROR",
                "error_code": "ERR_INVALID_NAME",
                "message": "Nama lengkap peserta tidak boleh kosong."
            }

        if cleaned_nik not in self.user_database:
            self.user_database[cleaned_nik] = {
                "name": cleaned_name,
                "claim_count": 0
            }

        current_claims = self.user_database[cleaned_nik]["claim_count"]
        if current_claims >= 3:
            return {
                "status": "REJECTED_QUOTA_EXCEEDED",
                "error_code": "ERR_MAX_CLAIM_REACHED",
                "message": "Batas maksimum klaim (3 item / 3x transaksi) untuk NIK ini telah habis."
            }

        try:
            steps_int = int(raw_steps)
            price_int = int(item_price)
        except (ValueError, TypeError):
            return {
                "status": "REJECTED_ERROR",
                "error_code": "ERR_DATATYPE_MISMATCH",
                "message": "Format jumlah langkah atau harga item harus berupa angka numerik."
            }

        item_lower = item_choice.lower()
        if "beras" in item_lower:
            price_int = self.kopdes_rice_price

        if price_int > self.max_redemption_cap:
            return {
                "status": "REJECTED_CAP_EXCEEDED",
                "error_code": "ERR_PRICE_ABOVE_LIMIT",
                "message": f"Harga item (Rp{price_int:,}) melampaui pagu batas maksimal Rp{self.max_redemption_cap:,}."
            }

        partner_share = max(float(negotiated_partner_share), self.min_partner_share)
        merchant_share = 0.15
        csr_share = round(1.0 - (partner_share + merchant_share), 4)

        effective_steps = min(steps_int, self.max_steps_per_user)
        total_claim_idr = float(min(effective_steps * self.conversion_rate, price_int))

        amount_partner = round(total_claim_idr * partner_share, 2)
        amount_csr = round(total_claim_idr * csr_share, 2)
        amount_merchant = round(total_claim_idr * merchant_share, 2)

        self.user_database[cleaned_nik]["claim_count"] += 1
        remaining_quota = 3 - self.user_database[cleaned_nik]["claim_count"]

        transaction_receipt = {
            "campaign": "September Sehat Grassroots Pilot 2026",
            "timestamp": datetime.now().isoformat(),
            "participant": cleaned_name,
            "nik_masked": f"{cleaned_nik[:6]}******{cleaned_nik[12:]}",
            "claim_sequence": self.user_database[cleaned_nik]["claim_count"],
            "remaining_quota": remaining_quota,
            "item_redeemed": item_choice,
            "item_price_idr": price_int,
            "verified_conversion_idr": total_claim_idr,
            "funding_allocation": {
                "partner_share_pct": f"{int(partner_share * 100)}%",
                "partner_amount_idr": amount_partner,
                "csr_central_pct": f"{int(csr_share * 100)}%",
                "csr_amount_idr": amount_csr,
                "merchant_adjustment_pct": "15%",
                "merchant_amount_idr": amount_merchant
            },
            "status_code": "SUCCESS_ZERO_ERROR_VERIFIED",
            "watermark_sig": "AL-HAQQ-PROTOCOL-ICAM"
        }

        return transaction_receipt

if __name__ == "__main__":
    engine = ZeroErrorRedemptionEngine()

    print("=== PENGUJIAN 1: KLAIM VALID BERAS KOPDES ===")
    res1 = engine.process_transaction(
        nik="3171234567890001",
        full_name="Siti Aminah",
        raw_steps=9000,
        item_choice="Beras Kopdes 3Kg",
        item_price=30000,
        negotiated_partner_share=0.20
    )
    print(json.dumps(res1, indent=4))

    print("\n=== PENGUJIAN 2: UJI COBA MANIPULASI NIK SALAH ===")
    res_err = engine.process_transaction(
        nik="12345",
        full_name="Budi",
        raw_steps=5000,
        item_choice="Minyak Goreng",
        item_price=20000
    )
    print(json.dumps(res_err, indent=4))


--- ICAM x AI DIGITAL WATERMARK ---
Timestamp: 2026-09-10 09:42:58.155184
Principle: Al-Haqq Protocol
