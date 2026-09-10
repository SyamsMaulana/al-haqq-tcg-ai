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
        self.max_allowed_claim = 1

    def _load_database(self):
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
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
            print("   (AL-HAQQ-PROTOCOL - SYSTEM ENGINE)")
            print("========================================")
            print("1. Proses Redeem / Hibah ke Guru Honorer")
            print("2. Cek Status e-KTP & Akumulasi Langkah")
            print("3. Audit Mingguan Dana Hibah Guru Honorer")
            print("4. Ekspor Laporan Rekap CSV")
            print("5. Simulasi Broadcast Ringkasan Otomatis")
            print("6. Keluar / Exit")
            
            choice = input("\nPilih menu (1-6): ").strip()
            
            if choice == "1":
                self.process_redeem_flow()
            elif choice == "2":
                self.check_status_flow()
            elif choice == "3":
                self.weekly_audit_flow()
            elif choice == "4":
                self.export_to_csv()
            elif choice == "5":
                self.broadcast_summary_simulation()
            elif choice == "6":
                print("\nTerima kasih! Program selesai. - AL-HAQQ-PROTOCOL-ICAM")
                break
            else:
                print("❌ Pilihan tidak valid. Silakan coba lagi.")

    def process_redeem_flow(self):
        print("\n--- FORMULIR REDEEM & HIBAH GURU HONORER ---")
        nik = input("Masukkan 16 digit NIK e-KTP pemberi/warga: ").strip()
        
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
                "last_date": "-",
                "status_penerima": "Mandiri (Warga)"
            }
            
        if self.user_db[nik]["claims"] >= self.max_allowed_claim:
            print(f"❌ DITOLAK: NIK atas nama '{self.user_db[nik]['name']}' sudah menggunakan hak 1x transaksinya.")
            return
            
        try:
            steps = int(input("Masukkan jumlah langkah Strava hari ini: ").strip())
        except ValueError:
            print("❌ Error: Jumlah langkah harus berupa angka!")
            return
            
        print("\nPilih Jenis Alokasi Subsidi:")
        print("1. Ambil Sembako Pribadi (Beras Kopdes Rp30.000)")
        print("2. Hibahkan / Sedekahkan ke Guru Honorer Terdaftar (Max Rp35.000)")
        pilihan_alur = input("Pilih nomor tujuan (1/2): ").strip()
        
        timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valid_steps = min(steps, self.max_steps)

        if pilihan_alur == "2":
            nama_guru = input("Masukkan Nama Guru Honorer Penerima Hibah: ").strip()
            asal_sekolah = input("Masukkan Asal Sekolah Guru Honorer: ").strip()
            if not nama_guru:
                nama_guru = "Guru Honorer Pengabdian"
            
            item_choice = f"Hibah ke Guru Honorer: {nama_guru} ({asal_sekolah})"
            item_price = self.max_cap
            self.user_db[nik]["status_penerima"] = f"Donatur Hibah untuk Guru: {nama_guru}"
        else:
            item_choice = "Beras Kopdes 3Kg"
            item_price = self.kopdes_rice_price
            self.user_db[nik]["status_penerima"] = "Penerima Sembako Mandiri"

        total_claim = float(min(valid_steps * self.conversion_rate, item_price))
        
        partner_share = 0.20
        merchant_share = 0.15
        csr_share = 1.0 - (partner_share + merchant_share)
        
        amt_partner = round(total_claim * partner_share, 2)
        amt_csr = round(total_claim * csr_share, 2)
        amt_merchant = round(total_claim * merchant_share, 2)

        self.user_db[nik]["claims"] += 1
        self.user_db[nik]["total_steps"] += valid_steps
        self.user_db[nik]["last_item"] = item_choice
        self.user_db[nik]["last_date"] = timestamp_now
        self._save_database()
        
        receipt = {
            "timestamp": timestamp_now,
            "participant": name,
            "nik_masked": f"{nik[:6]}******{nik[12:]}",
            "jenis_transaksi": "HIBAH GURU HONORER" if pilihan_alur == "2" else "SEMBAKO MANDIRI",
            "steps_contributed": valid_steps,
            "nominal_subsidi_idr": total_claim,
            "alokasi_pendanaan": {
                "partner_share": amt_partner,
                "csr_pool": amt_csr,
                "merchant_kopdes": amt_merchant
            },
            "status_code": "SUCCESS_VERIFIED_HAQQ",
            "watermark": "AL-HAQQ-PROTOCOL-ICAM"
        }
        
        print("\n========================================")
        print("    STRUK RESI DIGITAL TERVERIFIKASI    ")
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
            print(f"\nNama Warga        : {data['name']}")
            print(f"Status Penggunaan : {'Sudah Digunakan' if used >= 0 else 'Belum'}")
            print(f"Peran / Alokasi   : {data.get('status_penerima', '-')}")
            print(f"Akumulasi Langkah : {total_steps:,} langkah")
            print(f"Aktivitas Terakhir: {data.get('last_item', '-')}")
        else:
            print("ℹ️ NIK belum terdaftar dalam sistem.")

    def weekly_audit_flow(self):
        print("\n========================================")
        print("    AUDIT MINGGUAN DANA HIBAH GURU      ")
        print("========================================")
        
        total_hibah_dana = 0
        total_transaksi = 0
        daftar_hibah = []

        for nik, data in self.user_db.items():
            item = data.get("last_item", "")
            if "Hibah ke Guru Honorer" in item:
                total_transaksi += 1
                total_hibah_dana += self.max_cap
                daftar_hibah.append({
                    "donatur": data.get("name"),
                    "keterangan": item,
                    "waktu": data.get("last_date")
                })

        print(f"Total Transaksi Hibah Tercatat : {total_transaksi} transaksi")
        print(f"Akumulasi Dana Hibah Disalurkan: Rp {total_hibah_dana:,.0f}")
        print("-" * 40)
        if daftar_hibah:
            print("Rincian Penyaluran Ke Guru Honorer:")
            for idx, h in enumerate(daftar_hibah, 1):
                print(f"{idx}. Dari: {h['donatur']} | {h['keterangan']} | [{h['waktu']}]")
        else:
            print("ℹ️ Belum ada data hibah guru honorer yang tercatat pada siklus ini.")
        print("========================================\n")

    def broadcast_summary_simulation(self):
        print("\n========================================")
        print("   SIMULASI BROADCAST LAPORAN MINGGUAN  ")
        print("========================================")
        
        total_warga = len(self.user_db)
        total_langkah = sum(d.get("total_steps", 0) for d in self.user_db.values())
        total_hibah_count = sum(1 for d in self.user_db.values() if "Hibah ke Guru Honorer" in d.get("last_item", ""))
        total_dana_hibah = total_hibah_count * self.max_cap

        pesan_broadcast = f"""📢 *LAPORAN RESMI PILOT SEPTEMBER SEHAT* 📢
🗓️ Tanggal: {datetime.now().strftime('%Y-%m-%d')}
🏛️ Protokol: AL-HAQQ-PROTOCOL-ICAM

📊 *RINGKASAN AKUMULASI:*
- Total Warga Terdaftar : {total_warga} NIK
- Total Langkah Strava  : {total_langkah:,} langkah
- Total Hibah Guru      : {total_hibah_count} Transaksi
- Akumulasi Dana Disalurkan: Rp {total_dana_hibah:,.0f}

✨ _"Alhamdulillah life is good. Transparansi mutlak untuk kesejahteraan bersama dan pahlawan tanpa tanda jasa."_
---
*Pesan ini siap disalin untuk laporan grup WhatsApp / Aliansi.*
"""
        print(pesan_broadcast)
        print("========================================\n")

    def export_to_csv(self):
        csv_filename = f"laporan_audit_guru_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["NIK", "Nama Warga", "Status/Peran", "Total Klaim", "Akumulasi Langkah", "Aktivitas Terakhir", "Waktu"])
                for nik, data in self.user_db.items():
                    writer.writerow([
                        nik,
                        data.get("name"),
                        data.get("status_penerima"),
                        data.get("claims"),
                        data.get("total_steps"),
                        data.get("last_item"),
                        data.get("last_date")
                    ])
            print(f"\n✅ Berhasil! Laporan audit terekspor ke: {csv_filename}")
        except Exception as e:
            print(f"\n❌ Gagal mengekspor CSV: {e}")

if __name__ == "__main__":
    app = KopdesCLIApp()
    app.run()
