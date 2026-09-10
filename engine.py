import json

def load_config(filepath="config.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def evaluate_agents(config):
    print(f"--- Running {config["project_name"]} (v{config["version"]}) ---")
    print(f"Execution Environment: {config["architecture"]["execution_environment"]}\n")
    
    for agent in config["agents"]:
        print(f"Agent ID: {agent["id"]}")
        print(f"Role: {agent["role"]}")
        print(f"Active Strategies: {", ".join(agent["active_strategies"])}")
        print(f"Win Rate: {agent["performance_metrics"]["win_rate"] * 100}% ({agent["performance_metrics"]["matches_analyzed"]} matches)")
        print("-" * 40)

if __name__ == "__main__":
    config = load_config()
    evaluate_agents(config)
