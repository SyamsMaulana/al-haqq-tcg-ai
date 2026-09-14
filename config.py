




# Konfigurasi Aturan TCG AI - Casual Mode
GAME_MODE = "casual"
DECK_SIZE_LIMIT = 100
MAX_CARD_COPIES = 2
INITIAL_MANA_TURN_1 = 3
INITIAL_HAND_SIZE = 7
MAX_MULLIGAN_ATTEMPTS = 1

def validate_deck_composition(deck):
    """
    Memastikan dek mematuhi aturan 100 kartu dan maksimal 2 salinan per kartu.
    """
    if len(deck) != DECK_SIZE_LIMIT:
        return False, f"Jumlah total kartu harus tepat {DECK_SIZE_LIMIT} (saat ini: {len(deck)})."
    
    card_counts = {}
    for card in deck:
        card_id = card.get("id")
        card_counts[card_id] = card_counts.get(card_id, 0) + 1
        if card_counts[card_id] > MAX_CARD_COPIES:
            return False, f"Kartu '{card.get('name')}' melanggar batas maksimal ({MAX_CARD_COPIES} salinan)."
            
    return True, "Dek valid sesuai regulasi casual."

