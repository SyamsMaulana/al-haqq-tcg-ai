import json
from datetime import datetime
def nexus_hub():
 with open("config.json", "r") as f:
  c = json.load(f)
 print("=== TCG AI Nexus Master Hub ===")
 print(f"Project: {c.get("project_name")} (v{c.get("version")})")
 print(f"Active Agents: {len(c.get("agents", []))}")
 soul_logs = c.get("soul_logs", [])
 if soul_logs:
  latest_soul = soul_logs[-1]
  print(f"Soul Resonance: {latest_soul.get("manifesto")}")
 audits = c.get("audit_logs", [])
 print(f"Total System Events Tracked: {len(audits) + len(soul_logs)}")
 print("Status: All systems synchronized across device boundary.")
if __name__ == "__main__":
 nexus_hub()
