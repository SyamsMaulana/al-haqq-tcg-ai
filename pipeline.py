






import os
import sqlite3
import gc
import logging
import cv2
import onnxruntime as ort

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Optimasi Pre-processing OpenCV (Adaptive Thresholding & Kontur)
def preprocess_card_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Gambar tidak ditemukan atau korup: {image_path}")
    processed = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    return processed

# 2. Pengindeksan Tabel SQLite Lokal untuk Pencarian Instan
def optimize_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (card_id TEXT PRIMARY KEY, set_code TEXT, status TEXT, scanned_at TEXT);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_card_set ON inventory(card_id, set_code);")
    conn.commit()
    conn.close()

# 3. Pembersihan Memori Otomatis untuk Batch Scan
def cleanup_batch_memory():
    gc.collect()

# 4. Inisialisasi Sesi ONNX Runtime untuk Akselerasi Inferensi Visi
def load_onnx_model(model_path):
    options = ort.SessionOptions()
    options.intra_op_num_threads = 4
    if os.path.exists(model_path):
        session = ort.InferenceSession(model_path, options, providers=['CPUExecutionProvider'])
        return session
    return None

def run_tcg_ai_pipeline(image_folder, db_path, model_path):
    optimize_database(db_path)
    session = load_onnx_model(model_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    valid_extensions = ('.jpg', '.jpeg', '.png')
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)
        
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)]
    
    if not image_files:
        logging.warning(f"Tidak ada file gambar di folder '{image_folder}'. Masukkan sampel foto kartu (.jpg/.png) ke folder images/ terlebih dahulu.")
        conn.close()
        return
        
    logging.info(f"Memulai batch scan untuk {len(image_files)} gambar kartu...")
    
    for idx, filename in enumerate(image_files, 1):
        image_path = os.path.join(image_folder, filename)
        try:
            processed_img = preprocess_card_image(image_path)
            card_id = filename.split('.')[0]
            
            cursor.execute("""
                INSERT OR REPLACE INTO inventory (card_id, set_code, status, scanned_at)
                VALUES (?, ?, 'Pre-Graded', datetime('now'))
            """, (card_id, "GOD-TCG"))
            
            if idx % 10 == 0:
                conn.commit()
                cleanup_batch_memory()
                logging.info(f"Proses: {idx}/{len(image_files)} kartu tersimpan. Sesi pembersihan memori berjalan.")
                
        except Exception as e:
            logging.error(f"Gagal memproses file {filename}: {str(e)}")
            
    conn.commit()
    conn.close()
    logging.info("Seluruh rangkaian pemindaian batch dan sinkronisasi database selesai.")

if __name__ == "__main__":
    run_tcg_ai_pipeline(
        image_folder="images",
        db_path="tcg_inventory.db",
        model_path="model.onnx"
    )
