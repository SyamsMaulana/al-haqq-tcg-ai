







# deck_builder.py — Modul Validasi & Pembangunan Dek Kustom Al-Haqq TCG
import json
import deck_data
import agent_data

class DeckBuilder:
    def __init__(self, max_points=30):
        self.max_points = max_points
        self.deck_pool = deck_data.starter_deck_database + agent_data.karsa_agents_database
        self.current_deck = []

    def add_card_to_deck(self, card_id):
        card_obj = next((c for c in self.deck_pool if c.get('card_id') == card_id), None)
        if not card_obj:
            return False, "Kartu tidak ditemukan dalam basis data."
        
        if len(self.current_deck) >= 15:
            return False, "Batas maksimum dek adalah 15 kartu/agens."
            
        self.current_deck.append(card_obj)
        return True, f"Berhasil menambahkan {card_obj['name']} ke dalam dek."

    def validate_mizan_deck(self):
        count = len(self.current_deck)
        is_balanced = 10 <= count <= 15
        report = {
            "total_cards": count,
            "mizan_status": "SEIMBANG (Valid)" if is_balanced else "TIDAK SEIMBANG (Butuh 10-15 Kartu)",
            "deck_contents": [c['name'] for c in self.current_deck]
        }
        return report

if __name__ == "__main__":
    builder = DeckBuilder()
    builder.add_card_to_deck("AH-001")
    builder.add_card_to_deck("AG-001")
    print(builder.validate_mizan_deck())
