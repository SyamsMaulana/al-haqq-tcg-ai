import datetime
import zipfile
import os

SAFE_FILENAME = f"deep_digital_safe_tidore_{datetime.datetime.now().strftime('%Y%m%d')}.zip"
files = [
    "proposal_dapur_inspirasi_tidore.md", "surat_pengantar_tidore.md",
    "kampanye_gerbang_tidore.md", "ekspansi_pelabuhan_banda.md",
    "tracker_eksekusi_7_hari.md", "proposal_csr_swasta.md",
    "publikasi_gerbang_tidore.md", "nasi_goreng_garasi_blueprint.md"
]

with zipfile.ZipFile(SAFE_FILENAME, 'w', zipfile.ZIP_DEFLATED) as vault:
    for f in files:
        if os.path.exists(f): 
            vault.write(f)
            print(f"Berhasil menyegel: {f}")

print(f"Deep Digital Safe Sukses Terkunci: {SAFE_FILENAME}")
