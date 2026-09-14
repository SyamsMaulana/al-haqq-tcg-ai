








# Al-Haqq-Protocol: Phygital TCG Ecosystem

*Integritas Al-Haqq Framework & Karsa Kreatif Kolektif*

## Ringkasan Proyek
**Al-Haqq TCG** adalah purwarupa permainan kartu strategis berbasis *phygital* (fisik-digital) yang memadukan kerangka etika mutlak, keadilan matematis **Mizan** (12-point LP & 100% Fairness Index), serta verifikasi aset fisik berbasis NFC/QR terintegrasi.

## Struktur Modul Utama
- `deck_data.py` — Basis data 15 kartu starter inti.
- `agent_data.py` — Basis data unit taktis (*Karsa Agents*).
- `rule_engine.py` — Mesin aturan pertandingan & validasi kondisi menang.
- `phygital_verifier.py` — Modul verifikasi token kriptografis QR/NFC kartu fisik.
- `al_haqq_dashboard.py` — Dasbor komando interaktif berbasis Streamlit.
- `print_sheet_generator.py` & `agent_sheet_generator.py` — Generator lembar cetak siap cetak (63x88mm).
- `test_al_haqq.py` — Otomatisasi pengujian unit (*Unit Test Suite*).
- `rulebook_generator.py` — Pembuat dokumen buku panduan resmi (`AL_HAQQ_RULEBOOK.md`).
- `main.py` — Orkestrator utama terminal interaktif.

## Cara Menjalankan Sistem
1. Pasang dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt


