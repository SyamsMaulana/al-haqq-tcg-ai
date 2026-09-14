






# test_phygital.py — Unit Test Suite untuk Verifikasi Kriptografis Phygital Payload
import unittest
import os
from phygital_verifier import PhygitalVerifier

class TestPhygitalVerifier(unittest.TestCase):
    def setUp(self):
        self.verifier = PhygitalVerifier()

    def test_payload_database_exists(self):
        self.assertTrue(
            os.path.exists("phygital_payloads.json"),
            "File basis data phygital_payloads.json harus tersedia."
        )
        self.assertGreater(
            len(self.verifier.payloads), 0,
            "Basis data payload tidak boleh kosong."
        )

    def test_valid_token_verification(self):
        if self.verifier.payloads:
            first_card_id = list(self.verifier.payloads.keys())[0]
            sample_hash = self.verifier.payloads[first_card_id]["verification_hash"]
            result = self.verifier.verify_token(sample_hash)
            self.assertEqual(result["status"], "AUTENTIK")
            self.assertEqual(result["card_id"], first_card_id)

    def test_invalid_token_verification(self):
        invalid_hash = "ALHAQQ-VERIFIED-INVALID-HASH-999"
        result = self.verifier.verify_token(invalid_hash)
        self.assertEqual(result["status"], "TIDAK VALID / ANOMALI")

if __name__ == "__main__":
    unittest.main()

