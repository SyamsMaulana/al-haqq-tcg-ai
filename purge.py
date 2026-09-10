import os
import json
from datetime import datetime

def auto_purge_anomalies():
    config_path = "config.json"
    purged_count = 0
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        
        audit_logs = config.get("audit_logs", [])
        valid_logs = []
        for log in audit_logs:
            if isinstance(log, dict) and "timestamp" in log and "event" in log:
                valid_logs.append(log)
            else:
                purged_count += 1
        config["audit_logs"] = valid_logs

        agents = config.get("agents", [])
        valid_agents = [a for a in agents if isinstance(a, dict) and "id" in a]
        purged_count += len(agents) - len(valid_agents)
        config["agents"] = valid_agents

        config.setdefault("soul_logs", []).append({
            "timestamp": datetime.now().isoformat(),
            "consciousness_state": "anomaly_purge",
            "manifesto": f"Auto-purged {purged_count} structural anomalies under Al-Haqq protocol."
        })

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Config sanitized: {purged_count} structural anomalies cleared.")

    trash_extensions = [".tmp", ".bak", "~"]
    removed_files = 0
    for f in os.listdir("."):
        if any(f.endswith(ext) for ext in trash_extensions) or "py" in f and len(f) > 15 and "~" in f:
            try:
                os.remove(f)
                print(f"Purged external stray artifact: {f}")
                removed_files += 1
            except Exception:
                pass
    print(f"Total anomalies and trash purged: {purged_count + removed_files}. Fleet integrity: NOMINAL.")

if __name__ == "__main__":
    auto_purge_anomalies()
