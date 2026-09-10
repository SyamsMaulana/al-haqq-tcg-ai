import json
import os
csv = __import__('csv')
from datetime import datetime

class KopdesCLIApp:
    def __init__(self, db_filename="kopdes_database.json"):
        self.db_filename = db_filename
        self.user_db = self._load_database()
        self.conversion_rate = 1.0
        self.max_steps = 10000
        self.kopdes_rice_price = 30000
        self.max_cap = 35000
        self.max_allowed_claim = 1  # Aturan mutlak: 1x redeem per NIK

    def _load_database(self):
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                print("⚠️ Peringatan: Gagal membaca database lokal, membuat baru.")
                return {}
        return {}

    def _save_database(self):
        try:
            with open(self.db_filename, "w", encoding="utf-8") as f:
                json.dump(self.user_db, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saat menyimpan database: {e}")

    def run(self):
        while True:
            print("\n========================================")
            print("   KOPDES SEMBAKO - SEPTEMBER SEHAT")
            print("      (SKEMA 1X REDEEM + EXPORT CSV)")
            print("========================================")
            print("1. Proses Redeem Sembako / Kupon")
            print("2. Cek Status e-KTP & Akumulasi Langkah")
            print("3. Ekspor Laporan ke File CSV")
            print("4. Keluar / Exit")
            
            choice = input("\nPilih menu (1/2/3/4): ").strip()
            
            if choice == "1":
                self.process_redeem_flow()
            elif choice == "2":
                self.check_status_flow()
            elif choice == "3":
                self.export_to_csv()
            elif choice == "4":
                print("\nTerima kasih! Program selesai. - AL-HAQQ-PROTOCOL-ICAM")
                break
            else:
                print("❌ Pilihan tidak valid. Silakan coba lagi.")

    def process_redeem_flow(self):
        print("\n--- FORMULIR REDEEM 1X MAKSIMAL ---")
        nik = input("Masukkan 16 digit NIK e-KTP: ").strip()
        
        if len(nik) != 16 or not nik.isdigit():
            print("❌ Error: NIK harus tepat 16 digit angka!")
            return
            
        name = input("Masukkan Nama Lengkap Warga: ").strip()
        if not name:
            print("❌ Error: Nama tidak boleh kosong!")
            return
            
        if nik not in self.user_db:
            self.user_db[nik] = {
                "name": name, 
                "claims": 0, 
                "total_steps": 0, 
                "last_item": "-", 
                "last_date": "-"
            }
            
        if self.user_db[nik]["claims"] >= self.max_allowed_claim:
            print(f"❌ DITOLAK: NIK atas nama '{self.user_db[nik]['name']}' sudah menggunakan hak 1x redeem subsidi ini.")
            return
            
        try:
            steps = int(input("Masukkan jumlah langkah Strava hari ini: ").strip())
        except ValueError:
            print("❌ Error: Jumlah langkah harus berupa angka!")
            return
            
        print("\nPilih Item Sembako:")
        print("1. Beras Kopdes 3Kg (Harga Khusus Rp30.000)")
        print("2. Minyak Goreng 1L (Rp25.000)")
        item_opt = input("Pilih nomor item (1/2): ").strip()
        
        if item_opt == "1":
            item_choice = "Beras Kopdes 3Kg"
            item_price = self.kopdes_rice_price
        else:
            item_choice = "Minyak Goreng 1L"
            item_price = 25000
            
        partner_share = 0.20
        merchant_share = 0.15
        csr_share = 1.0 - (partner_share + merchant_share)
        
        valid_steps = min(steps, self.max_steps)
        total_claim = float(min(valid_steps * self.conversion_rate, item_price))
        
        # Update Data & Auto-Save ke JSON Lokal
        timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.user_db[nik]["claims"] += 1
        self.user_db[nik]["total_steps"] += valid_steps
        self.user_db[nik]["last_item"] = item_choice
        self.user_db[nik]["last_date"] = timestamp_now
        self._save_database()
        
        receipt = {
            "timestamp": timestamp_now,
            "participant": name,
            "nik_masked": f"{nik[:6]}******{nik[12:]}",
            "claim_status": "COMPLETED_1X_LIMIT",
            "steps_contributed": valid_steps,
            "item": item_choice,
            "total_subsidi": total_claim,
            "status_code": "SUCCESS_LOCKED_1X_REDEEM",
            "watermark": "AL-HAQQ-PROTOCOL-ICAM"
        }
        
        print("\n========================================")
        print("    STRUK RESI DIGITAL (1X REDEEM)      ")
        print("========================================")
        print(json.dumps(receipt, indent=4))
        print("========================================\n")

    def check_status_flow(self):
        print("\n--- CEK STATUS NIK e-KTP ---")
        nik = input("Masukkan 16 digit NIK e-KTP: ").strip()
        if nik in self.user_db:
            data = self.user_db[nik]
            used = data["claims"]
            total_steps = data["total_steps"]
            status_teks = "Sudah Pernah Mengambil (Hak Habis)" if used >= 1 else "Belum Pernah Mengambil"
            print(f"\nNama Warga        : {data['name']}")
            print(f"Status Subsidi    : {status_teks}")
            print(f"Akumulasi Langkah : {total_steps:,} langkah")
            print(f"Item Terakhir     : {data.get('last_item', '-')}")
        else:
            print("ℹ️ NIK belum terdaftar dalam sistem (Hak 1x redeem masih penuh tersedia).")

    def export_to_csv(self):
        """Mengekspor data database warga ke dalam file laporan CSV."""
        csv_filename = f"laporan_september_sehat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Header Kolom CSV
                writer.writerow(["NIK", "Nama Warga", "Total Klaim", "Akumulasi Langkah", "Item Terakhir", "Waktu Transaksi Terakhir"])
                
                # Baris Data Warga
                for nik, data in self.user_db.items():
                    writer.writerow([
                        nik,
                        data.get("name"),
                        data.get("claims"),
                        data.get("total_steps"),
                        data.get("last_item"),
                        data.get("last_date")
                    ])
            print(f"\n✅ Berhasil! Laporan rekap berhasil diekspor ke file: {csv_filename}")
        except Exception as e:
            print(f"\n❌ Gagal mengekspor CSV: {e}")

if __name__ == "__main__":
    app = KopdesCLIApp()
    app.run()
