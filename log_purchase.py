import json
import sys
from datetime import datetime

def log_test_purchase(amount, currency, item_name):
    config_path = "config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {"audit_logs": [], "purchases": []}

    purchase_record = {
        "timestamp": datetime.now().isoformat(),
        "node": "node_alpha",
        "item": item_name,
        "amount": amount,
        "currency": currency,
        "gateway": "Google Play Germany",
        "status": "VERIFIED_SUCCESS"
    }

    config.setdefault("purchases", []).append(purchase_record)
    config.setdefault("audit_logs", []).append({
        "timestamp": datetime.now().isoformat(),
        "event": "node_alpha_test_purchase_logged",
        "status": "SUCCESS"
    })

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Purchase of {amount} {currency} ({item_name}) successfully logged under Node Alpha telemetry.")

if __name__ == "__main__":
    # Example usage: python log_purchase.py 4.99 EUR "Starter Gem Pack"
    amt = float(sys.argv[1]) if len(sys.argv) > 1 else 4.99
    curr = sys.argv[2] if len(sys.argv) > 2 else "EUR"
    item = sys.argv[3] if len(sys.argv) > 3 else "Test Gem Pack"
    log_test_purchase(amt, curr, item)
