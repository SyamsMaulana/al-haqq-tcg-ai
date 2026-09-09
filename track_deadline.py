import datetime

START_DATE = datetime.date(2026, 9, 10)
DEADLINE_DAYS = 7
DEADLINE_DATE = START_DATE + datetime.timedelta(days=DEADLINE_DAYS)
today = datetime.date.today()
days_elapsed = (today - START_DATE).days
days_remaining = DEADLINE_DAYS - days_elapsed

STAMP = "\n\n--- [ICAM/Syams Maulana - Al-Haqq Protocol Collaboration Stamp] ---\nSistem Pelacakan Deadline 7 Hari & Protokol Eskalasi Swasta\nOtentisitas Dilindungi Prinsip Al-Haqq.\n"

status = "AUTO-CANCEL AKTIF: Alihkan ke Swasta!" if today > DEADLINE_DATE else f"Sisa waktu {days_remaining} hari menuju batas akhir."

report = f"# Tracker Eksekusi 7 Hari\nTanggal: {today}\nStatus: {status}\nDeadline: {DEADLINE_DATE}\n"
with open("tracker_eksekusi_7_hari.md", "w", encoding="utf-8") as f:
    f.write(report + STAMP)

print(f"Tracker diperbarui! Status: {status}")
