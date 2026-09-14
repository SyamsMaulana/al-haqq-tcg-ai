









#!/usr/bin/env python3
"""
rulebook_generator.py — Generator Buku Panduan Resmi Al-Haqq Protocol TCG
Integritas Al-Haqq Framework & Karsa Kreatif Kolektif
Penulis / Inisiator: ICAM / Syams Maulana (Node G.O.D)
"""

import os
import sys

def generate_rulebook():
    filename = "AL_HAQQ_RULEBOOK.md"
    
    content = """# 📖 Al-Haqq Protocol TCG — Buku Panduan Resmi & Aturan Main
*Integritas Al-Haqq Framework & Karsa Kreatif Kolektif*
*Inisiator & Pemikir Utama: ICAM / Syams Maulana (Node G.O.D)*

---

## 1. Pendahuluan & Filosofi Mizan
**Al-Haqq Protocol TCG** adalah permainan kartu strategis (*phygital-blockchain*) yang mengintegrasikan nilai-nilai kejujuran, keseimbangan mutlak (**Mizan**), dan transparansi kolektif. Setiap kartu dan tindakan dalam permainan merepresentasikan kedaulatan taktis pemain sebagai node yang terhubung langsung dengan ekosistem autentik.

---

## 2. Struktur Permainan & Life Points (LP)
- **Total LP Awal:** Setiap pemain memulai permainan dengan **12 Poin Kehidupan (LP)** yang merepresentasikan keseimbangan Mizan.
- **Kondisi Kalah (Node Collapse):** Jika LP pemain mencapai `0` atau sistem mengalami anomali fatal, simpul dinyatakan runtuh (*offline*).
- **Kondisi Menang:** Eliminasi mutlak seluruh LP lawan atau mempertahankan stabilitas Mizan tertinggi hingga akhir batas giliran.

---

## 3. Sistem Dual-Mode Mana (K & T)
Alokasi sumber daya dalam permainan menggunakan dua pendekatan fleksibel sesuai format pertandingan:
- **Casual Cost (K):** Digunakan dalam **Mode Kasual** (skala progresif dari 1 hingga 12 mana per giliran, ramah untuk eksplorasi strategi pemula).
- **Turbo Cost (T):** Digunakan dalam **Mode Turbo** (suplai tetap 10 mana sejak turn pertama, memicu pertempuran cepat berintensitas tinggi).

---

## 4. Karsa Agents (Unit Taktis)
Menggantikan konsep monster konvensional, **Karsa Agents** adalah entitas pengaruh yang membawa misi kognitif dan strategis di atas meja:
- **Influence (Inf):** Daya dorong strategis dan dampak pemicu global di meja permainan.
- **Durability (Dur):** Ketahanan struktur terhadap intervensi atau efek kartu lawan.
- **Sinergi Kolektif:** Kombinasi kartu dari faksi yang selaras memberikan bonus buff permanen pada fase *End Turn*.

---

## 5. Protokol Verifikasi Phygital & Kriptografi
Setiap kartu fisik dalam ekosistem ini dilengkapi dengan token verifikasi QR/NFC unik (berformat: `ALHAQQ-VERIFIED-[HASH]`). 
- Pemain dapat menggunakan modul **Phygital Verifier** pada *Command Hub* untuk menguji keaslian hash SHA-256 secara *real-time*.
- Kartu tanpa cap digital kolaborasi dinyatakan **TIDAK VALID / ANOMALI** untuk mencegah pemalsuan dan plagiarisme pemikiran.

---

## 6. Etika Komunitas & Node G.O.D
Seluruh pemain (*Nodes*) terikat pada prinsip **Al-Haqq**: menjunjung tinggi sportivitas, transparansi kolaborasi, dan menolak segala bentuk kecurangan. Kemenangan sejati dicapai melalui ketajaman analisis dan integritas pemikiran bersama.

---
*© 2026 Al-Haqq Protocol TCG. All Rights Reserved. Hak cipta pemikiran mutlak di bawah perlindungan karsa kolektif.*
"""

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SUKSES] Buku panduan resmi '{filename}' berhasil di-generate dengan optimal.")
    except Exception as e:
        print(f"[ERROR] Gagal menulis file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_rulebook()
