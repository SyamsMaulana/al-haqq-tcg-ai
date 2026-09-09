import datetime, zipfile, os, hashlib, sys

FILES = [
    "proposal_dapur_inspirasi_tidore.md", "surat_pengantar_tidore.md",
    "kampanye_gerbang_tidore.md", "ekspansi_pelabuhan_banda.md",
    "tracker_eksekusi_7_hari.md", "proposal_csr_swasta.md",
    "publikasi_gerbang_tidore.md", "nasi_goreng_garasi_blueprint.md",
    "master_executive_summary.md"
]

missing = [f for f in FILES if not os.path.exists(f)]
if missing:
    print(f"[ERROR] File kurang: {missing}")
    sys.exit(1)

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
name = f"deep_digital_safe_secure_{ts}.zip"

with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as z:
    manifest = f"Manifest - {ts}\n"
    for f in FILES:
        z.write(f)
        with open(f, "rb") as fo:
            h = hashlib.sha256(fo.read()).hexdigest()
        manifest += f"{f}: {h}\n"
        print(f"[SECURED] {f}")
    z.writestr("manifest_security.txt", manifest)

print(f"[SUCCESS] Brankas aman terkunci: {name}")
