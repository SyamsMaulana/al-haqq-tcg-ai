def calculate_threats(player_states):
    """
    Determines threat priority for Archenemy / Cooperative mode.
    player_states: list of dicts with keys: name, life, permanents_count, hand_size
    """
    scored_threats = []
    for p in player_states:
        score = (p.get('permanents_count', 0) * 2) + (p.get('hand_size', 0) * 1.5) + (40 - p.get('life', 40))
        scored_threats.append({
            "player": p.get('name'),
            "threat_score": score
        })
    scored_threats.sort(key=lambda x: x['threat_score'], reverse=True)
    return scored_threats
