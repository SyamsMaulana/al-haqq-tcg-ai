









import threading
import time
import random
import requests
from requests.exceptions import Timeout, RequestException
import deck_data

# Inisialisasi Lock Global untuk mencegah eksekusi ganda
portfolio_lock = threading.Lock()

print("Loaded TCG-AI-Automation-Framework successfully.")

def execute_portofolio_command():
    if not portfolio_lock.acquire(blocking=False):
        print("[System] Perintah Portofolio sebelumnya masih berjalan.")
        return "[Processing...] (Mohon tunggu, proses sebelumnya belum selesai)"
    try:
        print("[Processing...] Memulai kalkulasi valuasi dan sinkronisasi data...")
        target_url = "https://api.example.com/tcg-market-prices"
        
        try:
            response = requests.get(target_url, timeout=5)
            response.raise_for_status()
            market_data = response.json()
        except Timeout:
            print("Error: Koneksi melampaui batas waktu (timeout).")
            return "Error: Koneksi timeout saat mengambil data pasar."
        except RequestException as e:
            print(f"Error HTTP: {e}")
            return f"Error Gagal terhubung: {e}"
        
        total_valuasi = sum(item.get('price', 0) for item in market_data.get('cards', []))
        return f"Valuasi Selesai. Total: Rp {total_valuasi}"
        
    finally:
        portfolio_lock.release()

def execute_tcg_simulation():
    class PlayerNode:
        def __init__(self, player_id, mode="casual"):
            self.player_id = player_id
            self.lp = 12
            self.mode = mode
            self.mana = 10 if mode == "turbo" else 1
            self.hand = []
            self.is_active = True

        def draw_card(self, database):
            card = random.choice(database)
            self.hand.append(card)

    class PhygitalMatch:
        def __init__(self, num_players, mode="casual"):
            self.num_players = num_players
            self.mode = mode
            self.players = [PlayerNode(i, mode) for i in range(num_players)]
            self.turn = 0

        fn = None
        def simulate_turns(self, turns=5):
            for _ in range(turns):
                self.turn += 1
                for p in self.players:
                    if not p.is_active:
                        continue
                    if self.mode == "casual":
                        p.mana = min(self.turn, 12)
                    p.draw_card(deck_data.starter_deck_database)
                    playable = [c for c in p.hand if (p.mana >= c['casual_cost'] if self.mode == "casual" else p.mana >= c['turbo_cost'])]
                    if playable:
                        for opp in self.players:
                            if opp.player_id != p.player_id and opp.is_active:
                                opp.lp -= 1
                                if opp.lp <= 0:
                                    opp.is_active = False

    match = PhygitalMatch(num_players=4, mode="casual")
    match.simulate_turns(5)
    
    result_log = f"[Simulasi Berhasil] Turn {match.turn} tercapai untuk 4 Node.\n"
    for p in match.players:
        result_log += f"Player {p.player_id}: LP = {p.lp}, Kartu di Tangan = {len(p.hand)}\n"
    return result_log

def handle_user_input(command_text):
    cleaned_cmd = command_text.strip().title()
    if cleaned_cmd == "Portofolio":
        return execute_portofolio_command()
    elif cleaned_cmd == "Simulasi":
        return execute_tcg_simulation()
    return f"Command tidak dikenal: {command_text}"

if __name__ == "__main__":
    print("Al-Haqq TCG Hub aktif dan berjalan di localhost:8080...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
