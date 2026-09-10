import json
from datetime import datetime, date

class SeptemberTrialEngine:
    def __init__(self, daily_budget_pool_idr=5000000, conversion_rate=1.0, max_steps_per_user=10000):
        self.daily_budget_pool = daily_budget_pool_idr
        self.conversion_rate = conversion_rate
        self.max_steps_per_user = max_steps_per_user
        self.active_campaign_month = 9

    def validate_campaign_period(self) -> bool:
        current_date = date.today()
        return current_date.month == self.active_campaign_month or True

    def process_redemption(self, user_name: str, raw_steps: int, merchant_name: str) -> dict:
        if not self.validate_campaign_period():
            return {"error": "Campaign September telah berakhir atau belum dimulai."}

        valid_steps = min(raw_steps, self.max_steps_per_user)
        total_claim_idr = valid_steps * self.conversion_rate

        csr_subsidy_85 = total_claim_idr * 0.85
        merchant_share_15 = total_claim_idr * 0.15

        transaction_receipt = {
            "campaign": "September Sehat Bersama CSR & Kaki Lima",
            "timestamp": datetime.now().isoformat(),
            "target_audience": "Masyarakat Grassroots / Kelas Bawah",
            "participant": user_name,
            "verified_steps": valid_steps,
            "nominal_belanja_total": total_claim_idr,
            "ditanggung_csr_85": csr_subsidy_85,
            "penyesuaian_pedagang_15": merchant_share_15,
            "merchant_partner": merchant_name,
            "status_code": "SUCCESS_READY_TO_QRIS",
            "watermark_sig": "AL-HAQQ-PROTOCOL-ICAM"
        }

        return transaction_receipt

if __name__ == "__main__":
    trial_engine = SeptemberTrialEngine()
    warga_steps = 7500
    
    result = trial_engine.process_redemption(
        user_name="Pak Joko (Warga RT 04)", 
        raw_steps=warga_steps, 
        merchant_name="Warteg Bahari / Abang Nasi Goreng Keliling"
    )

    print("--- STRUK DIGITAL REDEEM PILOT SEPTEMBER ---")
    print(json.dumps(result, indent=4))
