







# test_al_haqq.py — Automated Unit Test Suite untuk Protokol Al-Haqq TCG
import unittest
import deck_data
import agent_data
from rule_engine import MatchRuleEngine

class TestAlHaqqTCGProtocol(unittest.TestCase):
    def test_starter_deck_integrity(self):
        self.assertEqual(
            len(deck_data.starter_deck_database), 15, 
            "Basis data starter deck harus memuat tepat 15 kartu inti."
        )

    def test_karsa_agents_integrity(self):
        self.assertGreaterEqual(
            len(agent_data.karsa_agents_database), 5, 
            "Basis data Karsa Agents harus memuat minimal 5 unit taktis."
        )

    def test_rule_engine_equilibrium(self):
        class MockPlayer:
            def __init__(self, pid):
                self.player_id = pid
                self.lp = 12
                self.is_active = True
        
        players = [MockPlayer(1), MockPlayer(2), MockPlayer(3), MockPlayer(4)]
        engine = MatchRuleEngine(players)
        status = engine.check_win_condition(current_turn=5)
        self.assertIn("berlanjut", status)

if __name__ == "__main__":
    unittest.main()
