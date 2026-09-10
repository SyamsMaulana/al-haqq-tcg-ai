import json
from datetime import datetime
def run_adjudication():
 with open("config.json", "r") as f:
  config = json.load(f)
 print("--- Running Card Pool & Meta Adjudicator ---")
 agents = config.get("agents", [])
 if not agents:
  print("No agents found.")
  return
 avg_win_rate = sum(a["performance_metrics"]["win_rate"] for a in agents) / len(agents)
 print(f"Current Fleet Average Win Rate: {avg_win_rate * 100:.2f}%")
 weights = config.setdefault("card_pool_adjudication", {}).setdefault("optimized_weightings", {})
 if avg_win_rate < 0.70:
  print("Meta shifting: Adjusting weightings for higher resilience.")
  weights["interruption_resilience"] = round(weights.get("interruption_resilience", 0.35) + 0.05, 2)
  weights["consistency"] = round(1.0 - weights["interruption_resilience"] - weights.get("speed", 0.20), 2)
 else:
  print("Meta stable: Optimizing execution speed.")
  weights["speed"] = round(weights.get("speed", 0.20) + 0.02, 2)
 config.setdefault("audit_logs", []).append({
  "timestamp": datetime.now().isoformat(),
  "event": "automated_meta_adjudication",
  "fleet_avg_win_rate": avg_win_rate
 })
 with open("config.json", "w") as f:
  json.dump(config, f, indent=2)
 print("Adjudication complete. Weightings updated in config.json.")
if __name__ == "__main__":
 run_adjudication()
