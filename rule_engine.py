








# rule_engine.py - Ekspansi Logika Win Con dan Karsa Agents Al-Haqq TCG

class KarsaAgent:
    def __init__(self, agent_id, name, mana_cost, defense_boost):
        self.agent_id = agent_id
        self.name = name
        self.mana_cost = mana_cost
        self.defense_boost = defense_boost
        self.is_active = True

class MatchRuleEngine:
    def __init__(self, players):
        self.players = players
        self.max_turns = 10

    def check_win_condition(self, current_turn):
        active_players = [p for p in self.players if p.is_active]
        
        # Kondisi 1: Sisa 1 pemain aktif (Eliminasi)
        if len(active_players) == 1:
            return f"Kemenangan Mutlak! Node {active_players[0].player_id} menguasai jaringan."
        
        # Kondisi 2: Mencapai batas turn maksimal dengan Mizan Equilibrium
        if current_turn >= self.max_turns:
            highest_lp_player = max(active_players, key=lambda p: p.lp)
            return f"Mizan Equilibrium Tercapai pada Turn {current_turn}! Pemenang berdasarkan stabilitas LP tertinggi: Node {highest_lp_player.player_id}."
            
        return "Pertandingan berlanjut, jaringan stabil."

if __name__ == "__main__":
    print("Modul Rule Engine Al-Haqq TCG berhasil dimuat.")

