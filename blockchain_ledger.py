





#!/usr/bin/env python3
"""
blockchain_ledger.py — Ledger Kriptografis Blok Mutlak untuk Al-Haqq Protocol TCG
Integritas Al-Haqq Framework & Karsa Kreatif Kolektif
Inisiator & Pemikir Utama: ICAM / Syams Maulana (Node G.O.D)
"""

import hashlib
import json
import os
import datetime

class AlHaqqLedger:
    def __init__(self, ledger_file="al_haqq_blockchain.json"):
        self.ledger_file = ledger_file
        self.chain = self.load_ledger()

    def load_ledger(self):
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return [self.create_genesis_block()]
        else:
            return [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_block = {
            "index": 0,
            "timestamp": str(datetime.datetime.now()),
            "data": {
                "message": "Genesis Block — Al-Haqq Protocol TCG Mizan Integrity",
                "initiator": "ICAM / Syams Maulana"
            },
            "previous_hash": "0" * 64
        }
        genesis_block["hash"] = self.calculate_hash(genesis_block)
        return genesis_block

    def calculate_hash(self, block):
        block_string = json.dumps({
            "index": block["index"],
            "timestamp": block["timestamp"],
            "data": block["data"],
            "previous_hash": block["previous_hash"]
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, transaction_data):
        last_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": str(datetime.datetime.now()),
            "data": transaction_data,
            "previous_hash": last_block["hash"]
        }
        new_block["hash"] = self.calculate_hash(new_block)
        self.chain.append(new_block)
        self.save_ledger()
        print(f"[BLOCKCHAIN] Blok #{new_block['index']} berhasil ditambang & diverifikasi Mizan.")
        return new_block

    def save_ledger(self):
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(self.chain, f, indent=4)

    def verify_integrity(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current["previous_hash"] != previous["hash"]:
                return False
            if current["hash"] != self.calculate_hash(current):
                return False
        return True

if __name__ == "__main__":
    ledger = AlHaqqLedger()
    ledger.add_block({"type": "MATCH_RESULT", "winner": "Node A", "loser": "Node B", "mizan_score": "12-8"})
    print(f"Status Integritas Blockchain Ledger: {'VALID (Mizan Terjaga)' if ledger.verify_integrity() else 'ANOMALI TERDETEKSI'}")

