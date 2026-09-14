





# tournament_manager.py — Modul Manajemen Turnamen & Papan Peringkat Node G.O.D TCG
import json
import os

class TournamentManager:
    def __init__(self, tournament_name="G.O.D Season 1: Mizan Cup"):
        self.tournament_name = tournament_name
        self.standings = {}

    def register_node(self, node_id, player_name):
        self.standings[node_id] = {
            "player_name": player_name,
            "wins": 0,
            "losses": 0,
            "mizan_score": 100.0,
            "status": "Active"
        }

    def record_match(self, winner_node, loser_node):
        if winner_node in self.standings and loser_node in self.standings:
            self.standings[winner_node]["wins"] += 1
            self.standings[loser_node]["losses"] += 1
            self.standings[winner_node]["mizan_score"] = round(100.0 - (self.standings[winner_node]["losses"] * 2.5), 2)
            self.standings[loser_node]["mizan_score"] = round(100.0 - (self.standings[loser_node]["losses"] * 2.5), 2)

    def export_standings(self):
        report = {
            "tournament": self.tournament_name,
            "standings": self.standings
        }
        with open("tournament_standings.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        print(f"Papan peringkat turnamen '{self.tournament_name}' berhasil diekspor.")

if __name__ == "__main__":
    tm = TournamentManager()
    tm.register_node("NODE-01", "GOD•MauL")
    tm.register_node("NODE-02", "KarsaNode_X")
    tm.record_match("NODE-01", "NODE-02")
    tm.export_standings()

