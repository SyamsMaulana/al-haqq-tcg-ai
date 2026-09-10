import json

def show_fleet_dashboard():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json tidak ditemukan.")
        return

    print("=" * 55)
    print("🛡️  AL-HAQQ TCG-AI FLEET TELEMETRY (CLI DASHBOARD)")
    print("=" * 55)
    print(f"Project : {config.get("project_name")}")
    print(f"Version : {config.get("version")}")
    
    agents = config.get("agents", [])
    total_matches = sum(a["performance_metrics"]["matches_analyzed"] for a in agents) if agents else 0
    fleet_avg_win = (sum(a["performance_metrics"]["win_rate"] for a in agents) / len(agents)) if agents else 0.0

    print(f"\n📊 Ringkasan Sistem:")
    print(f" - Total Agen Terdaftar     : {len(agents)}")
    print(f" - Total Pertandingan Dianalisis : {total_matches}")
    print(f" - Rata-rata Win Rate Fleet  : {fleet_avg_win:.2%}")

    print("\n" + "-" * 55)
    print("🤖 Matriks Performa Agen:")
    if agents:
        for a in agents:
            m = a["performance_metrics"]
            print(f" • ID        : {a["id"]}")
            print(f"   Archetype : {a.get("archetype", "N/A")}")
            print(f"   Matches   : {m["matches_analyzed"]}")
            print(f"   Win Rate  : {m["win_rate"]:.2%}")
            print("-" * 40)
    else:
        print(" (Tidak ada agen terdaftar)")

    print("\n📜 Audit Logs Terbaru:")
    audit_logs = config.get("audit_logs", [])
    if audit_logs:
        for log in audit_logs[-3:]:
            print(f" [{log.get("timestamp")}] {log.get("event")} -> Agent: {log.get("agent", "N/A")} | Hasil: {log.get("result", "N/A")}")
    else:
        print(" (Belum ada audit log)")

    print("\n✨ Soul Log & Manifesto Terakhir:")
    soul_logs = config.get("soul_logs", [])
    if soul_logs:
        latest = soul_logs[-1]
        print(f" [{latest.get("timestamp")}] State: {latest.get("consciousness_state")}")
        print(f" Manifesto : {latest.get("manifesto")}")
    else:
        print(" (Belum ada soul log)")
    print("=" * 55)

if __name__ == "__main__":
    show_fleet_dashboard()
