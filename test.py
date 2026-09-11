



import threading
import requests
from requests.exceptions import Timeout, RequestException

# Menggunakan threading.Lock untuk mencegah eksekusi ganda (race condition)
processing_lock = threading.Lock()

def process_portofolio_command():
    # Cek apakah proses sedang berjalan tanpa menunggu (non-blocking)
    if not processing_lock.acquire(blocking=False):
        return {
            "status": "busy",
            "message": "Perintah sebelumnya masih diproses. Harap tunggu hingga selesai."
        }
    
    try:
        print("[Processing...] Memulai kalkulasi valuasi dan sinkronisasi data...")
        
        # Batasan waktu (timeout) pada permintaan eksternal atau scraping
        target_url = "https://api.example.com/tcg-market-prices"
        
        try:
            response = requests.get(target_url, timeout=5) # Timeout diatur 5 detik
            response.raise_for_status()
            market_data = response.json()
        except Timeout:
            print("Error: Koneksi melampaui batas waktu (timeout).")
            return {"status": "error", "message": "Koneksi timeout saat mengambil data pasar."}
        except RequestException as e:
            print(f"Error HTTP: {e}")
            return {"status": "error", "message": f"Gagal terhubung: {e}"}
        
        # Simulasi kalkulasi data binder atau JSON lokal
        total_valuasi = sum(item.get('price', 0) for item in market_data.get('cards', []))
        
        return {
            "status": "success",
            "valuasi": total_valuasi,
            "data": market_data
        }
        
    finally:
        # Blok finally menjamin lock selalu dilepaskan meskipun terjadi error
        processing_lock.release()
