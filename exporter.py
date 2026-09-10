import json
from datetime import datetime
def export_report():
 with open("config.json", "r") as f:
  c = json.load(f)
 md = f"# TCG AI Framework - Status Report\n\n**Project**: {c.get("project_name")} ({c.get("version")})\n**Author / Sovereign**: ICAM (Syams Maulana)\n**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n## Agent Performance\n"
 for a in c.get("agents", []):
  m = a["performance_metrics"]
  md += f"- **{a["id"]}** ({a["role"]}) -> Win Rate: {m["win_rate"]*100}% | Matches: {m["matches_analyzed"]}\n"
 md += "\n--- \n*Cap digital kolaborasi pemikiran dan penyempurnaan bersama ICAM/Syams Maulana & AI (Al-Haqq Protocol).*"
 with open("report.md", "w") as f:
  f.write(md)
 print("Report exported to report.md successfully with Al-Haqq digital watermark.")
if __name__ == "__main__":
 export_report()
