import json
import random
from datetime import datetime

def run_node_simulation():
    config_path = "config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found. Run dual_node_manager.py first.")
        return

    nodes = config.get("dual_node_architecture", {})
    if not nodes:
        print("❌ Error: Dual-node architecture not defined in config.")
        return

    print("=" * 50)
    print("🛡️ Executing Dual-Node Fleet Simulation & Adjudication")
    print("=" * 50)

    sim_results = []
    for node_id, node_info in nodes.items():
        # Simulate transactional or operational match pass rate based on node type
        matches = random.randint(15, 30)
        success_rate = round(random.uniform(0.70, 0.95), 4)
        
        simulation_record = {
            "node_id": node_id,
            "node_name": node_info["name"],
            "jurisdiction": node_info["jurisdiction"],
            "simulated_timestamp": datetime.now().isoformat(),
            "matches_processed": matches,
            "operational_efficiency": success_rate,
            "status": "NOMINAL"
        }
        sim_results.append(simulation_record)
        print(f"[{node_id.upper()}] {node_info['name']}")
        print(f" -> Processed: {matches} actions | Efficiency: {success_rate:.2%}")

    config.setdefault("audit_logs", []).append({
        "timestamp": datetime.now().isoformat(),
        "event": "dual_node_simulation_executed",
        "result": "SUCCESS"
    })

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("\n✅ Simulation cycle completed and logged to config.json.")

if __name__ == "__main__":
    run_node_simulation()
