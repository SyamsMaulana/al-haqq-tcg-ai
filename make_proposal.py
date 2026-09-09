#!/usr/bin/env python3
import datetime

STAMP = "\n\n--- [ICAM/Syams Maulana - Al-Haqq Protocol Collaboration Stamp] ---\nProyek: Dapur Inspirasi & Ekspedisi Tidore\nOtentisitas Dilindungi Prinsip Al-Haqq.\n"

content = "# Dapur Inspirasi: Ekspedisi Kuliner Tidore\nTanggal: " + str(datetime.date.today()) + "\n\n## 1. Tujuan\nMengubah potensi rempah dan pangan maritim Tidore menjadi produk siap-guna bagi komunitas lokal.\n"

with open("proposal_dapur_inspirasi_tidore.md", "w", encoding="utf-8") as f:
    f.write(content + STAMP)
print("Proposal Tidore Berhasil Dibuat!")
