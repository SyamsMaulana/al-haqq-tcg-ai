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
