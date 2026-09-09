import datetime

STAMP = "\n\n--- [ICAM/Syams Maulana - Al-Haqq Protocol Collaboration Stamp] ---\nKampanye: Tidore sebagai Gerbang Pembuka Indonesia Timur\nOtentisitas Dilindungi Prinsip Al-Haqq.\n"

CAMPAIGN = f"""# Dapur Inspirasi: Tidore sebagai Gerbang Pembuka Ekspedisi Nusantara Timur
Tanggal Publikasi: {datetime.date.today().strftime('%d %B %Y')}

## 1. Esensi Gerbang Pembuka
Tidore bukan sekadar destinasi tunggal, melainkan titik nol dan **gerbang pembuka** kultural-kuliner. Dari tanah rempah bersejarah inilah mata rantai peradaban maritim Indonesia Timur mulai diikat, sebelum nantinya langkah ekspedisi merambat menjamah tanah-tanah agung lainnya di kawasan timur nusantara.

## 2. Konsep Visual & Narasi Digital
- **Visual Utama:** Lanskap rempah pesisir Tidore berpadu dengan aktivitas dapur autentik, memancarkan kehangatan tradisi lokal yang berakar kuat.
- **Tone & Manner:** Tegas, membumi, sarat rasa syukur, dan berwibawa.
- **Call to Action (CTA):** Menyaksikan kebangkitan kedaulatan pangan dari timur, dimulai dari Tidore untuk Indonesia.
"""

with open("kampanye_gerbang_tidore.md", "w", encoding="utf-8") as f:
    f.write(CAMPAIGN + STAMP)

print("Modul Kampanye Gerbang Tidore Berhasil Dibuat!")
