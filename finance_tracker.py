import json
from datetime import datetime

def track_finances():
    config_path = "config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found.")
        return

    # Sample transaction reconciliation ledger for Dual-Node Architecture
    ledger_entries = [
        {
            "transaction_id": "TXN-2026-001",
            "node_id": "node_alpha",
            "item": "In-App Gem Pack (Local Store)",
            "amount_local": 49.99,
            "currency": "EUR",
            "estimated_tax_vat": 9.50,
            "fx_fee": 0.75,
            "status": "RECONCILED"
        },
        {
            "transaction_id": "TXN-2026-002",
            "node_id": "node_omega",
            "item": "Web Store Exclusive Bundle",
            "amount_local": 30.00,
            "currency": "USD",
            "estimated_tax_vat": 0.00,
            "fx_fee": 1.20,
            "status": "RECONCILED"
        }
    ]

    config["financial_ledger"] = ledger_entries

    config.setdefault("audit_logs", []).append({
        "timestamp": datetime.now().isoformat(),
        "event": "financial_reconciliation_executed",
        "total_transactions": len(ledger_entries),
        "status": "SUCCESS"
    })

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("=" * 50)
    print("💰 Financial Reconciliation Ledger Updated")
    print("=" * 50)
    for entry in ledger_entries:
        total_cost = entry["amount_local"] + entry["estimated_tax_vat"] + entry["fx_fee"]
        print(f" • [{entry['transaction_id']}] {entry['node_id'].upper()} | {entry['item']}")
        print(f"   Base: {entry['amount_local']} {entry['currency']} | Tax/VAT: {entry['estimated_tax_vat']} | FX Fee: {entry['fx_fee']}")
        print(f"   Total Net Deduction: {total_cost:.2f} {entry['currency']}")
        print("-" * 40)

if __name__ == "__main__":
    track_finances()
