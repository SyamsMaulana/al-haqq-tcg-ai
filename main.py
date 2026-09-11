






import threading
import time
import requests
from requests.exceptions import Timeout, RequestException

# Inisialisasi Lock Global untuk mencegah eksekusi ganda
portfolio_lock = threading.Lock()

print("Loaded TCG-AI-Automation-Framework successfully.")

def execute_portofolio_command():
    if not portfolio_lock.acquire(blocking=False):
        print("[System] Perintah Portofolio sebelumnya masih berjalan.")
        return "[Processing...] (Mohon tunggu, proses sebelumnya belum selesai)"

    try:
        print("[Processing...] Memulai kalkulasi valuasi dan sinkronisasi data...")
        target_url = "https://api.example.com/tcg-market-prices"

        try:
            response = requests.get(target_url, timeout=5)
            response.raise_for_status()
            market_data = response.json()
        except Timeout:
            print("Error: Koneksi melampaui batas waktu (timeout).")
            return "Error: Koneksi timeout saat mengambil data pasar."
        except RequestException as e:
            print(f"Error HTTP: {e}")
            return f"Error Gagal terhubung: {e}"

        total_valuasi = sum(item.get('price', 0) for item in market_data.get('cards', []))
        return f"Valuasi Selesai. Total: Rp {total_valuasi}"

    finally:
        portfolio_lock.release()

def handle_user_input(command_text):
    cleaned_cmd = command_text.strip().title()
    if cleaned_cmd == "Portofolio":
        return execute_portofolio_command()
    return f"Command tidak dikenal: {command_text}"

if __name__ == "__main__":
    print("Al-Haqq TCG Hub aktif dan berjalan di localhost:8080...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
