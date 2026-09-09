import datetime

STAMP = "\n\n--- [ICAM/Syams Maulana - Al-Haqq Protocol Collaboration Stamp] ---\nDokumen: Draf Proposal Cepat Sektor Swasta / CSR\nOtentisitas Dilindungi Prinsip Al-Haqq.\n"

CSR = f"""# Proposal Kemitraan Strategis & CSR: "Dapur Inspirasi & Ekspedisi Tidore"
Tanggal: {datetime.date.today().strftime('%d %B %Y')}

## 1. Pengantar Eksekusi Cepat
Program **"Dapur Inspirasi & Ekspedisi Tidore"** dirancang sebagai model pembangunan ekonomi akar rumput yang cepat, terukur, dan berdampak langsung. Melalui pendekatan kolaborasi swasta/CSR, kita memotong rantai birokrasi yang lambat demi menghadirkan aksi nyata di tanah rempah Tidore sebagai gerbang pembuka Indonesia Timur.

## 2. Nilai Strategis bagi Mitra Swasta (CSR Value)
- **Direct Impact:** Pelatihan vokasi kuliner langsung bagi pemuda lokal dan pelaku usaha mikro.
- **Brand Association:** Keterlibatan dalam pelestarian warisan budaya maritim dan kedaulatan pangan nasional.
- **High Agility:** Eksekusi langsung tanpa hambatan administratif yang berkepanjangan.

Hormat kami,

**Syams Maulana (ICAM)**  
Inisiator Dapur Inspirasi
"""

with open("proposal_csr_swasta.md", "w", encoding="utf-8") as f:
    f.write(CSR + STAMP)

print("Proposal CSR Swasta Berhasil Dibuat!")
