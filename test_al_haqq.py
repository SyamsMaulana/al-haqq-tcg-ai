











#!/usr/bin/env python3
"""
test_al_haqq.py — Unit Testing Suite untuk Al-Haqq Protocol TCG
Integritas Al-Haqq Framework & Karsa Kreatif Kolektif
Inisiator & Pemikir Utama: ICAM / Syams Maulana (Node G.O.D)
"""

import pytest
import os
import deck_data
import agent_data
from phygital_verifier import PhygitalVerifier
from deck_builder import DeckBuilder
from blockchain_ledger import AlHaqqLedger

def test_starter_deck_integrity():
    assert len(deck_data.starter_deck_database) == 15, "Basis data starter deck harus memuat tepat 15 kartu inti."

def test_karsa_agents_integrity():
    assert len(agent_data.karsa_agents_database) >= 5, "Basis data Karsa Agents harus memuat minimal 5 unit taktis."

def test_phygital_verifier_anomaly():
    verifier = PhygitalVerifier()
    result = verifier.verify_token("ALHAQQ-VERIFIED-INVALID-HASH")
    assert result["status"] == "TIDAK VALID / ANOMALI"

def test_deck_builder_add_and_validate():
    builder = DeckBuilder()
    builder.deck = []  # Reset dek lokal untuk pengujian
    success, _ = builder.add_card_to_deck("AH-001")
    assert success is True
    report = builder.validate_mizan_deck()
    assert report["total_cards"] == 1

def test_blockchain_ledger_integrity():
    test_file = "test_ledger_temp.json"
    if os.path.exists(test_file):
        os.remove(test_file)
        
    ledger = AlHaqqLedger(ledger_file=test_file)
    initial_len = len(ledger.chain)
    
    ledger.add_block({"type": "UNIT_TEST", "status": "VERIFIED"})
    assert len(ledger.chain) == initial_len + 1
    assert ledger.verify_integrity() is True
    
    if os.path.exists(test_file):
        os.remove(test_file)
