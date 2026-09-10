import json
import os
import csv
from datetime import datetime

class AlHaqqKopdesEngine:
    """
    Engine Utama: KOPDES SEMBAKO - SEPTEMBER SEHAT (v4.0)
    Protocol: AL-HAQQ-PROTOCOL-ICAM (Autentik, Transparan, & Visual Analytics)
    """
    def __init__(self, db_filename="kopdes_database.json"):
        self.db_filename = db_filename
        self.conversion_rate = 1.0
        self.max_steps = 10000
        self.kopdes_rice_price = 30000
        self.max_cap = 35000
        self.max_allowed_claim = 1
        self.user_db = self._load_database()

    def _load_database(self):
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print("⚠️ Peringatan: Database lokal korup. Menginisialisasi state bersih...")
                return {}
        return {}

    def _save_database(self):
        try:
            with open(self.db_filename, "w", encoding="utf-8") as f:
                json.dump(self.user_db, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error kritis saat menyimpan database: {e}")

    def run(self):
        while True:
            print("\n==================================================")
            print("   KOPDES SEMBAKO - SEPTEMBER SEHAT (v4.0)")
            print("   [AL-HAQQ-PROTOCOL-ICAM: ADVANCED ANALYTICS]")
            print("==================================================")
            print("1. Proses Redeem / Hibah (Auto Strava API Sync)")
            print("2. Cek Status e-KTP & Riwayat Historis Lintas Hari")
            print("3. Audit Mingguan & Grafik Analitik Terminal")
            print("4. Ekspor Laporan Rekap (CSV & JSON Resmi)")
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
                self.export_reports()
            elif choice == "5":
                self.broadcast_summary_simulation()
            elif choice == "6":
                print("\nAlhamdulillah. Sesi selesai. - AL-HAQQ-PROTOCOL-ICAM")
                break
            else:
                print("❌ Pilihan tidak valid. Masukkan angka 1 sampai 6.")

    def _mock_strava_api_fetch(self):
        print("\n[MOCKING API] Menghubungkan ke Strava OAuth Endpoint...")
        mock_payload = {
            "status": "SUCCESS",
            "athlete_id": "ICAM_STRAVA_SYNC_99",
            "activity_date": datetime.now().strftime("%Y-%m-%d"),
            "total_steps_recorded": 9200,
            "source": "Strava Mobile GPS Protocol"
        }
        print(f"🔌 Payload diterima dari Strava: {mock_payload['total_steps_recorded']:,} langkah")
        return mock_payload['total_steps_recorded']

    def process_redeem_flow(self):
        print("\n--- FORMULIR REDEEM & HIBAH (STRAVA API SYNC) ---")
        nik = input("Masukkan 16 digit NIK e-KTP pemberi/warga: ").strip()
        
        if len(nik) != 16 or not nik.isdigit():
            print("❌ Error: NIK harus tepat 16 digit angka!")
            return
            
        name = input("Masukkan Nama Lengkap Warga: ").strip()
        if not name:
            print("❌ Error: Nama tidak boleh kosong!")
            return
            
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        if nik not in self.user_db:
            self.user_db[nik] = {
                "name": name, 
                "claims": 0, 
                "total_steps": 0, 
                "history_logs": [],
                "status_penerima": "Mandiri (Warga)",
                "watermark_sig": "ICAM-AL-HAQQ"
            }
            
        if self.user_db[nik]["claims"] >= self.max_allowed_claim:
            print(f"❌ DITOLAK: NIK atas nama '{self.user_db[nik]['name']}' sudah menggunakan hak 1x kuota transaksinya secara permanen.")
            return
            
        print("\nSumber Data Langkah:")
        print("1. Input Manual Mandiri")
        print("2. Tarik Otomatis dari Strava API (Mocking Endpoint)")
        metode_langkah = input("Pilih metode (1/2): ").strip()
        
        if metode_langkah == "2":
            steps = self._mock_strava_api_fetch()
        else:
            try:
                steps = int(input("Masukkan jumlah langkah Strava hari ini: ").strip())
            except ValueError:
                print("❌ Error: Jumlah langkah harus berupa angka bulat!")
                return
            
        print("\nPilih Jenis Alokasi Subsidi:")
        print("1. Ambil Sembako Pribadi (Beras Kopdes Rp30.000)")
        print("2. Hibahkan ke Guru Honorer Terdaftar (Max Rp35.000)")
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
            self.user_db[nik]["status_penerima"] = f"Donatur Hibah untuk: {nama_guru}"
        else:
            item_choice = "Beras Kopdes 3Kg"
            item_price = self.kopdes_rice_price
            self.user_db[nik]["status_penerima"] = "Penerima Sembako Mandiri"

        total_claim = float(min(valid_steps * self.conversion_rate, item_price))
        
        partner_share = 0.20
        merchant_share = 0.15
        csr_share = 1.0 - (partner_share + merchant_share)
        
        self.user_db[nik]["claims"] += 1
        self.user_db[nik]["total_steps"] += valid_steps
        
        log_entry = {
            "date": today_date,
            "timestamp": timestamp_now,
            "item": item_choice,
            "steps": valid_steps,
            "nominal": total_claim
        }
        self.user_db[nik]["history_logs"].append(log_entry)
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
                "partner_share": round(total_claim * partner_share, 2),
                "csr_pool": round(total_claim * csr_share, 2),
                "merchant_kopdes": round(total_claim * merchant_share, 2)
            },
            "status_code": "SUCCESS_VERIFIED_HAQQ",
            "watermark": "AL-HAQQ-PROTOCOL-ICAM"
        }
        
        print("\n==================================================")
        print("    STRUK RESI DIGITAL TERVERIFIKASI (HAQQ)       ")
        print("==================================================")
        print(json.dumps(receipt, indent=4))
        print("==================================================\n")

    def check_status_flow(self):
        print("\n--- CEK STATUS NIK & RIWAYAT HISTORIS LINTAS HARI ---")
        nik = input("Masukkan 16 digit NIK e-KTP: ").strip()
        if nik in self.user_db:
            data = self.user_db[nik]
            print(f"\nNama Warga        : {data['name']}")
            print(f"Status Kuota      : {'Sudah Terpakai (1/1)' if data['claims'] > 0 else 'Tersedia'}")
            print(f"Peran / Alokasi   : {data.get('status_penerima', '-')}")
            print(f"Akumulasi Langkah : {data['total_steps']:,} langkah")
            print(f"Total Transaksi   : {len(data.get('history_logs', []))} sesi tercatat")
            
            logs = data.get("history_logs", [])
            if logs:
                print("\n📅 Riwayat Log Aktivitas Lintas Waktu:")
                for idx, log in enumerate(logs, 1):
                    print(f"  {idx}. Tanggal: {log['date']} | Item: {log['item']} | Langkah: {log['steps']:,}")
        else:
            print("ℹ️ NIK belum terdaftar di dalam database lokal.")

    def weekly_audit_flow(self):
        print("\n==================================================")
        print("    AUDIT MINGGUAN & GRAFIK ANALITIK TERMINAL     ")
        print("==================================================")
        
        total_hibah_dana = 0
        total_transaksi = 0
        mandiri_count = 0
        hibah_count = 0
        daftar_hibah = []

        for nik, data in self.user_db.items():
            if "Mandiri" in data.get("status_penerima", ""):
                mandiri_count += 1
            for log in data.get("history_logs", []):
                if "Hibah ke Guru Honorer" in log.get("item", ""):
                    total_transaksi += 1
                    hibah_count += 1
                    total_hibah_dana += self.max_cap
                    daftar_hibah.append({
                        "donatur": data.get("name"),
                        "keterangan": log["item"],
                        "waktu": log["timestamp"]
                    })

        print(f"Total Warga Partisipan     : {len(self.user_db)}")
        print(f"Total Sembako Mandiri      : {mandiri_count} warga")
        print(f"Total Hibah Guru Honorer   : {hibah_count} transaksi")
        print(f"Akumulasi Dana Disalurkan  : Rp {total_hibah_dana:,.0f}")
        
        print("\n📊 Grafik Proporsi Alokasi (ASCII Analytics):")
        total_pilihan = max(mandiri_count + hibah_count, 1)
        bar_mandiri = "█" * int((mandiri_count / total_pilihan) * 20)
        bar_hibah = "█" * int((hibah_count / total_pilihan) * 20)
        print(f"  Mandiri  [{bar_mandiri:<20}] {mandiri_count}")
        print(f"  Hibah    [{bar_hibah:<20}] {hibah_count}")
        
        print("-" * 50)
        if daftar_hibah:
            print("Rincian Penyaluran Ke Guru Honorer:")
            for idx, h in enumerate(daftar_hibah, 1):
                print(f"{idx}. Donatur: {h['donatur']} | {h['keterangan']} | [{h['waktu']}]")
        else:
            print("ℹ️ Belum ada data hibah guru honorer yang tercatat pada siklus ini.")
        print("==================================================\n")

    def broadcast_summary_simulation(self):
        print("\n==================================================")
        print("   SIMULASI BROADCAST LAPORAN MINGGUAN            ")
        print("==================================================")
        
        total_warga = len(self.user_db)
        total_langkah = sum(d.get("total_steps", 0) for d in self.user_db.values())
        
        total_hibah_count = 0
        for d in self.user_db.values():
            for log in d.get("history_logs", []):
                if "Hibah ke Guru Honorer" in log.get("item", ""):
                    total_hibah_count += 1
                    
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
*Pesan ini tersertifikasi otentik kolaborasi pemikiran ICAM.*
"""
        print(pesan_broadcast)
        print("==================================================\n")

    def export_reports(self):
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"laporan_audit_{timestamp_str}.csv"
        json_filename = f"laporan_audit_{timestamp_str}.json"
        
        try:
            # Ekspor CSV
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["NIK_Masked", "Nama Warga", "Status/Peran", "Total Klaim", "Akumulasi Langkah", "Aktivitas Terakhir", "Waktu", "Watermark"])
                for nik, data in self.user_db.items():
                    masked_nik = f"{nik[:6]}******{nik[12:]}" if len(nik) == 16 else nik
                    writer.writerow([
                        masked_nik,
                        data.get("name"),
                        data.get("status_penerima"),
                        data.get("claims"),
                        data.get("total_steps"),
                        data.get("last_item", "-"),
                        data.get("last_date", "-"),
                        data.get("watermark_sig", "ICAM-AL-HAQQ")
                    ])
            
            # Ekspor JSON Ringkas Resmi
            summary_payload = {
                "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "protocol": "AL-HAQQ-PROTOCOL-ICAM",
                "total_registered_users": len(self.user_db),
                "database_snapshot": self.user_db
            }
            with open(json_filename, "w", encoding="utf-8") as jf:
                json.dump(summary_payload, jf, indent=4, ensure_ascii=False)
                
            print(f"\n✅ Berhasil! Laporan audit terekspor bersih ke:\n - {csv_filename}\n - {json_filename}")
        except Exception as e:
            print(f"\n❌ Gagal mengekspor laporan: {e}")

if __name__ == "__main__":
    engine = AlHaqqKopdesEngine()
    engine.run()
