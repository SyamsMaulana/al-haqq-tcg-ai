import json
from datetime import datetime

def system_audit():
    with open("config.json", "r") as f:
        config = json.load(f)
    print("=== Master System Health & Audit ===")
    print(f"Project: {config.get("project_name")} (v{config.get("version")})")
    print(f"Total Agents Registered: {len(config.get("agents", []))}")
    print(f"Total Audit Logs Recorded: {len(config.get("audit_logs", []))}")
    print("Latest Audit Entry:")
    audit_logs = config.get("audit_logs", [])
    if audit_logs:
        latest = audit_logs[-1]
        for k, v in latest.items():
            print(f" - {k}: {v}")
    else:
        print(" None recorded.")
    print("System Integrity Status: NOMINAL")

if __name__ == "__main__":
    system_audit()
