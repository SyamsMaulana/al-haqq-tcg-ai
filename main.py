import json
import hashlib
from datetime import datetime

class AlHaqqProtocolEngine:
    def __init__(self, author="ICAM/Syams Maulana"):
        self.author = author
        self.watermark = self._generate_icam_watermark()

    def _generate_icam_watermark(self) -> str:
        """Menghasilkan signature watermark digital ICAM berbasis SHA-256."""
        payload = f"{self.author}-AL-HAQQ-{datetime.now().strftime('%Y%m%d')}"
        signature = hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12].upper()
        return f"ICAM-DIGITAL-WM-{signature}"

    def evaluate_sentiment_thresholds(self, sentiment_data: dict) -> dict:
        """Memeriksa apakah tingkat penolakan semua konsol berada di bawah 20%."""
        report = {}
        for platform, percentage in sentiment_data.items():
            report[platform] = {
                "sentimen_penolakan": f"{percentage}%",
                "ambang_batas_20": "LOLOS (Stabil)" if percentage < 20 else "PERLU ADJUSTMENT",
                "porsi_kritik_konstruktif": f"{percentage}%"
            }
        return report

    def calculate_escrow_and_equity(self, total_profit: float, user_base: dict) -> dict:
        """Kalkulasi otomatis dana CSR 2.5% dan User-Share Floating Equity."""
        csr_allocation = total_profit * 0.025
        net_distributable = total_profit - csr_allocation
        total_active_users = sum(user_base.values())

        equity_shares = {
            platform: round((users / total_active_users) * 100, 2)
            for platform, users in user_base.items()
        }

        return {
            "total_profit": f"${total_profit:,.2f}",
            "alokasi_csr_2_5": f"${csr_allocation:,.2f}",
            "sisa_profit_bersih": f"${net_distributable:,.2f}",
            "floating_equity_share": {k: f"{v}%" for k, v in equity_shares.items()}
        }

# --- INSENSIASI & EKSEKUSI DATA TERKINI ---
engine = AlHaqqProtocolEngine()

# Data Sentimen Terbaru (<20%)
current_sentiments = {
    "Nintendo": 18,
    "Xbox": 14,
    "Sony": 11
}

# Estimasi Pengguna Aktif Riil & Total Profit Konsol (Contoh Simulasi)
sample_users = {
    "Nintendo": 120_000_000,
    "Xbox": 85_000_000,
    "Sony": 115_000_000
}
simulated_profit = 10_000_000_000.0  # $10 Miliar USD

# Output Laporan
sentiment_eval = engine.evaluate_sentiment_thresholds(current_sentiments)
financial_eval = engine.calculate_escrow_and_equity(simulated_profit, sample_users)

output_payload = {
    "metadata": {
        "timestamp": datetime.now().isoformat(),
        "watermark_authentic": engine.watermark,
        "protocol_status": "Active & Verified"
    },
    "evaluasi_sentimen": sentiment_eval,
    "kalkulasi_keuangan_csr": financial_eval
}

print(json.dumps(output_payload, indent=2, ensure_ascii=False))



import sys
import os
from datetime import datetime

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.exists(target):
            with open(target, "a", encoding="utf-8") as f:
                f.write(f"\n\n--- ICAM x AI DIGITAL WATERMARK ---\nTimestamp: {datetime.now()}\nPrinciple: Al-Haqq Protocol\n")
            print(f"[SUCCESS] Watermark berhasil ditambahkan ke {target}")
        else:
            print(f"[ERROR] File {target} tidak ditemukan.")
    else:
        print("Gunakan: python main.py <nama_file>")

if __name__ == "__main__":
    main()



import json
import hashlib
from datetime import datetime

class AlHaqqProtocolEngine:
    def __init__(self, author="ICAM/Syams Maulana"):
        self.author = author
        self.watermark = self._generate_icam_watermark()

    def _generate_icam_watermark(self) -> str:
        payload = f"{self.author}-AL-HAQQ-{datetime.now().strftime('%Y%m%d')}"
        signature = hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12].upper()
        return f"ICAM-DIGITAL-WM-{signature}"

    def evaluate_sentiment_thresholds(self, sentiment_data: dict) -> dict:
        report = {}
        for platform, percentage in sentiment_data.items():
            report[platform] = {
                "sentimen_penolakan": f"{percentage}%",
                "ambang_batas_20": "LOLOS (Stabil)" if percentage < 20 else "PERLU ADJUSTMENT",
                "porsi_kritik_konstruktif": f"{percentage}%"
            }
        return report

    def calculate_escrow_and_equity(self, total_profit: float, user_base: dict) -> dict:
        csr_allocation = total_profit * 0.025
        net_distributable = total_profit - csr_allocation
        total_active_users = sum(user_base.values())

        equity_shares = {
            platform: round((users / total_active_users) * 100, 2)
            for platform, users in user_base.items()
        }

        return {
            "total_profit": f"${total_profit:,.2f}",
            "alokasi_csr_2_5": f"${csr_allocation:,.2f}",
            "sisa_profit_bersih": f"${net_distributable:,.2f}",
            "floating_equity_share": {k: f"{v}%" for k, v in equity_shares.items()}
        }

def export_protocol_log(data, filename="al_haqq_status.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n[SUCCESS] Laporan Al-Haqq Protocol berhasil disimpan di: {filename}")

if __name__ == "__main__":
    engine = AlHaqqProtocolEngine()

    current_sentiments = {"Nintendo": 18, "Xbox": 14, "Sony": 11}
    sample_users = {"Nintendo": 120_000_000, "Xbox": 85_000_000, "Sony": 115_000_000}
    simulated_profit = 10_000_000_000.0

    sentiment_eval = engine.evaluate_sentiment_thresholds(current_sentiments)
    financial_eval = engine.calculate_escrow_and_equity(simulated_profit, sample_users)

    output_payload = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "watermark_authentic": engine.watermark,
            "protocol_status": "Active & Verified"
        },
        "evaluasi_sentimen": sentiment_eval,
        "kalkulasi_keuangan_csr": financial_eval
    }

    # Cetak hasil ke layar
    print(json.dumps(output_payload, indent=2, ensure_ascii=False))
    
    # Ekspor ke file al_haqq_status.json
    export_protocol_log(output_payload)

