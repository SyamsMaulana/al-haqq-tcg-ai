



def evaluate_starting_hand(hand, max_initial_mana=3):
    """
    Mengevaluasi apakah tangan awal valid untuk dimainkan pada giliran pertama 
    berdasarkan batas mana awal (3 mana) untuk dek 100 kartu.
    """
    playable_cards = [card for card in hand if card.cost <= max_initial_mana]
    
    if len(playable_cards) == 0:
        return "MULLIGAN_REQUIRED"  # Tangan kosong dari kartu murah, wajib mulligan
    return "KEEP_HAND"

def execute_ai_mulligan(deck, hand_size=7):
    """
    Menjalankan proses pengambilan kartu awal dan pemeriksaan mulligan otomatis untuk agen AI.
    """
    import random
    hand = random.sample(deck, hand_size)
    decision = evaluate_starting_hand(hand)
    
    if decision == "MULLIGAN_REQUIRED":
        # Kocok kembali tangan ke dek dan ambil ulang
        deck.extend(hand)
        random.shuffle(deck)
        hand = random.sample(deck, hand_size)
        
    return hand

