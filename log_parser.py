

import re
from collections import defaultdict

# Log pertandingan Team True GOD sesuai data log
game_logs_raw = """
• G1: [T]akmauL *W – L* L Ikan
• G2: [T]akmauL *L – WR* L Ikan
• G3: [T]akmauL *L – WR* L Ikan
• G4: [T]Gobz *W – LR* L Ikan
• G5: [T]Gobz *L – W* L ROXA
• G6: [T]Gobz *W – L* L ROXA
• G7: [T]Gobz *W – L* L ROXA
• G8: [T]Gobz *W – L* [L]Havoc
• G9: [T]Gobz *W – LR* [L]Havoc
• G10: [T]Gobz *L – W* Char[L]otte
• G11: Tgus-aQIRA *L – W* Char[L]otte
• G12: Tgus-aQIRA *L – W* Char[L]otte
• G13: [T]yrogue *L – W* Char[L]otte
• G14: [T]yrogue *WR – L* Char[L]otte
• G15: [T]yrogue *WR – L* Char[L]otte
• G16: [T]yrogue *WR – L* Alyzter
• G17: [T]yrogue *LR – W* Alyzter
"""

def parse_and_calculate_stats(logs):
    player_stats = defaultdict(lambda: {"matches": 0, "wins": 0, "losses": 0})
    
    # Regular expression untuk memparsing baris log pertandingan
    pattern = re.compile(r'•\s*(G\d+):\s*(.*?)\s*\*(.*?)\s*–\s*(.*?)\*\s*(.*)')
    
    lines = logs.strip().split('\n')
    for line in lines:
        match = pattern.search(line)
        if match:
            game_id, player, p1_res, p2_res, opponent = match.groups()
            player = player.strip()
            
            player_stats[player]["matches"] += 1
            
            # Evaluasi hasil (W/WR vs L/LR)
            if 'W' in p1_res and 'L' not in p1_res or 'WR' in p1_res:
                player_stats[player]["wins"] += 1
            else:
                player_stats[player]["losses"] += 1

    return player_stats

def generate_reward_report(stats):
    print("=" * 65)
    print("       TEAM TRUE GOD: GAME LOGS & REWARD ALLOCATION REPORT      ")
    print("=" * 65)
    print(f"{'Player':<15} | {'Matches':<8} | {'Wins':<6} | {'Losses':<8} | {'Reward Status'}")
    print("-" * 65)
    
    for player, data in stats.items():
        matches = data["matches"]
        wins = data["wins"]
        losses = data["losses"]
        
        # Alokasi Booster x2 untuk seluruh anggota, MVP x3 khusus untuk [T]Gobz
        reward = "Booster x2"
        if "Gobz" in player:
            reward += " + MVP x3"
            
        print(f"{player:<15} | {matches:<8} | {wins:<6} | {losses:<8} | {reward}")
    print("=" * 65)

if __name__ == "__main__":
    stats = parse_and_calculate_stats(game_logs_raw)
    generate_reward_report(stats)


