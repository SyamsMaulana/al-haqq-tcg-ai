import datetime

STAMP = "\n\n--- [ICAM/Syams Maulana - Al-Haqq Protocol Collaboration Stamp] ---\nDokumen: Surat Pengantar Resmi Dapur Inspirasi Tidore\nOtentisitas Dilindungi Prinsip Al-Haqq.\n"

LETTER = f"""# Surat Pengantar Resmi: Permohonan Dukungan & Kolaborasi Program "Dapur Inspirasi & Ekspedisi Tidore"
Tanggal: {datetime.date.today().strftime('%d %B %Y')}

Kepada Yth.
Pimpinan Instansi / Mitra Strategis Terkait
dhi. Bidang Kebudayaan & Pemberdayaan

Dengan hormat,

Seiring dengan komitmen bersama dalam merawat warisan budaya nusantara dan memperkuat kedaulatan pangan berbasis kearifan lokal, melalui surat ini kami menyampaikan proposal program **"Dapur Inspirasi & Ekspedisi Tidore"**.

Program ini memadukan eksplorasi kekayaan rempah serta pangan maritim Kepulauan Tidore dengan pelatihan vokasi praktis di tingkat akar rumput. Seluruh gagasan disusun secara otentik di bawah *Al-Haqq Protocol* untuk memastikan integritas intelektual.

Besar harapan kami untuk dapat menjalin sinergi dan dukungan bersama instansi yang Bapak/Ibu pimpin.

Hormat kami,

**Syams Maulana (ICAM)**  
Inisiator Dapur Inspirasi
"""

with open("surat_pengantar_tidore.md", "w", encoding="utf-8") as f:
    f.write(LETTER + STAMP)

print("Surat Pengantar Tidore Berhasil Dibuat!")
