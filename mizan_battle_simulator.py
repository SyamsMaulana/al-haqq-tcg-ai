








#!/usr/bin/env python3
"""
mizan_battle_simulator.py — Simulasi Pertandingan & Validasi Keadilan Mizan (12-LP)
Integritas Al-Haqq Framework & Karsa Kreatif Kolektif
Inisiator & Pemikir Utama: ICAM / Syams Maulana (Node G.O.D)
"""

import random
import sys
import deck_data
import agent_data

class MizanBattleSimulator:
    def __init__(self, mode="Casual"):
        self.mode = mode  # "Casual" (Progresif 1-12) atau "Turbo" (Tetap 10)
        self.node_a_lp = 12
        self.node_b_lp = 12
        self.turn = 1

    def simulate_turn(self):
        print(f"\n--- Turn {self.turn} ({self.mode} Mode) ---")
        
        # Alokasi Mana berdasarkan Mode Mizan
        if self.mode == "Casual":
            mana_a = min(self.turn, 12)
            mana_b = min(self.turn, 12)
        else:  # Turbo Mode
            mana_a = 10
            mana_b = 10

        # Simulasi aksi acak terbobot Mizan untuk Node A & Node B
        damage_a = random.randint(1, 4) if mana_a >= 3 else 0
        damage_b = random.randint(1, 4) if mana_b >= 3 else 0

        self.node_b_lp = max(0, self.node_b_lp - damage_a)
        self.node_a_lp = max(0, self.node_a_lp - damage_b)

        print(f"Node A (Mana: {mana_a}) menyerang, menghasilkan {damage_a} DMG. LP Node B tersisa: {self.node_b_lp}/12")
        print(f"Node B (Mana: {mana_b}) menyerang, menghasilkan {damage_b} DMG. LP Node A tersisa: {self.node_a_lp}/12")
        
        self.turn += 1

    def run_match(self):
        print(f"⚖️ Memulai Simulasi Mizan Battle ({self.mode} Mode) — Al-Haqq Protocol TCG")
        while self.node_a_lp > 0 and self.node_b_lp > 0 and self.turn <= 10:
            self.simulate_turn()

        print("\n=== HASIL AKHIR PERTANDINGAN ===")
        if self.node_a_lp > self.node_b_lp:
            print(f"🏆 Node A Menang! Sisa Mizan LP: {self.node_a_lp}/12")
        elif self.node_b_lp > self.node_a_lp:
            print(f"🏆 Node B Menang! Sisa Mizan LP: {self.node_b_lp}/12")
        else:
            print("🤝 Pertandingan Berakhir Imbang (Mizan Seimbang Sempurna).")

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "Casual"
    simulator = MizanBattleSimulator(mode=mode_arg)
    simulator.run_match()
