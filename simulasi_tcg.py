






import random

class Player:
    def __init__(self, player_id, mode="casual"):
        self.player_id = player_id
        self.lp = 12
        self.mode = mode
        self.mana = 10 if mode == "turbo" else 1
        self.is_active = True

    def update_mana(self, turn_number):
        if self.mode == "casual":
            self.mana = min(turn_number, 12)
        else:
            self.mana = 10

class GameSimulation:
    def __init__(self, num_players, mode="casual"):
        self.num_players = num_players
        self.mode = mode
        self.players = [Player(i, mode) for i in range(num_players)]
        self.turns_elapsed = 0

    def run_match(self):
        while sum(1 for p in self.players if p.is_active) > 1 and self.turns_elapsed < 150:
            self.turns_elapsed += 1
            for player in self.players:
                if not player.is_active:
                    continue
                
                player.update_mana(self.turns_elapsed)
                
                # Global Generic Trigger Event (Symmetrical impact)
                if random.random() < 0.20:
                    trigger_damage = 1
                    for opponent in self.players:
                        if opponent.player_id != player.player_id and opponent.is_active:
                            opponent.lp -= trigger_damage
                            if opponent.lp <= 0:
                                opponent.is_active = False

                opponents = [p for p in self.players if p.player_id != player.player_id and p.is_active]
                if opponents:
                    target = random.choice(opponents)
                    strike_damage = min(random.randint(1, 3), max(1, player.mana // 3))
                    target.lp -= strike_damage
                    if target.lp <= 0:
                        target.is_active = False

            active_players = [p for p in self.players if p.is_active]
            if len(active_players) <= 1:
                break

        winner = [p.player_id for p in self.players if p.is_active]
        return self.turns_elapsed, winner

def run_comparative_simulations(num_simulations=300):
    modes = ["casual", "turbo"]
    for mode in modes:
        print(f"\n--- SIMULASI MODE: {mode.upper()} ---")
        print(f"{'Players':<10} | {'Avg Turns':<12} | {'Est. Duration':<15} | {'Fairness Index':<15}")
        print("-" * 60)
        
        for n in range(2, 9):
            total_turns = 0
            decisive_wins = 0
            for _ in range(num_simulations):
                sim = GameSimulation(n, mode)
                turns, winner = sim.run_match()
                total_turns += turns
                if len(winner) == 1:
                    decisive_wins += 1
                    
            avg_turns = total_turns / num_simulations
            fairness_index = (decisive_wins / num_simulations) * 100
            print(f"{n}-Player  | {avg_turns:<12.1f} | {avg_turns * 0.5:<6.1f} mins       | {fairness_index:<14.2f}%")

if __name__ == "__main__":
    print("=== AL-HAQQ FRAMEWORK: DUAL-MODE MANA & MULTIPLAYER SIMULATION ===")
    run_comparative_simulations(300)
