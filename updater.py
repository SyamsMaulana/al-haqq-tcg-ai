import json

def update_agent_metrics(agent_id, new_wins_delta, new_matches_delta, filepath="config.json"):
    with open(filepath, "r") as f:
        config = json.load(f)
    
    updated = False
    for agent in config["agents"]:
        if agent["id"] == agent_id:
            metrics = agent["performance_metrics"]
            total_matches = metrics["matches_analyzed"] + new_matches_delta
            current_wins = metrics["win_rate"] * metrics["matches_analyzed"]
            new_wins = current_wins + new_wins_delta
            
            metrics["matches_analyzed"] = total_matches
            metrics["win_rate"] = round(new_wins / total_matches, 4) if total_matches > 0 else 0.0
            updated = True
            break
            
    if updated:
        with open(filepath, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Metrics for {agent_id} successfully updated and saved.")
    else:
        print(f"Agent {agent_id} not found.")

if __name__ == "__main__":
    # Simulasi penambahan hasil match untuk agent_alpha (misal: menang 1 match baru dari 1 pertandingan)
    update_agent_metrics("agent_alpha", new_wins_delta=1, new_matches_delta=1)
