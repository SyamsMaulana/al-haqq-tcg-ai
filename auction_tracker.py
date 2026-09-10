import json
import datetime
import hashlib

def run_auction_tracker():
    timestamp = datetime.datetime.utcnow().isoformat()
    watermark_raw = f"ICAM-AUCTION-AL-HAQQ-{timestamp}"
    watermark_hash = f"ICAM-DIGITAL-WM-{hashlib.sha256(watermark_raw.encode()).hexdigest()[:12].upper()}"

    # Oracle Rate
    gold_spot_usd = 85.00   # 1 ICAM-G = 1 Gram Emas 24K
    silver_spot_usd = 1.00  # 1 ICAM-S = 1 Gram Perak Murni

    auction_items = [
        {
            "id": "AUC-001",
            "item_name": "Hermès Koala Print Silk Tie",
            "highest_bid_usd": 238.00,
            "bidder": "Collector_01",
            "target_allocation": "Commercial Pastry Mixer 10L Komunitas",
            "status": "Active Bidding"
        },
        {
            "id": "AUC-002",
            "item_name": "Max Raab American Flags Vintage Tie",
            "highest_bid_usd": 127.50,
            "bidder": "Collector_07",
            "target_allocation": "Artisan Deck Oven & Pizza Stone Setup",
            "status": "Active Bidding"
        },
        {
            "id": "AUC-003",
            "item_name": "Goldlion 1500 Special Edition Tie",
            "highest_bid_usd": 102.00,
            "bidder": "Collector_03",
            "target_allocation": "Set Pisau Chef & Talenan Vokasi",
            "status": "Active Bidding"
        },
        {
            "id": "AUC-004",
            "item_name": "Koleksi Memorabilia & Aksesori Vintage",
            "highest_bid_usd": 297.50,
            "bidder": "Collector_09",
            "target_allocation": "Bahan Baku & Equipment Vokasi Kuliner",
            "status": "In Preparation"
        }
    ]

    # Kalkulasi nilai Bimetallic ICAM Currency
    total_usd_raised = 0.0
    for item in auction_items:
        bid_usd = item["highest_bid_usd"]
        total_usd_raised += bid_usd
        item["icam_gold_value"] = f"{bid_usd / gold_spot_usd:.4f} ICAM-G"
        item["icam_silver_value"] = f"{bid_usd / silver_spot_usd:.2f} ICAM-S"

    log_data = {
        "metadata": {
            "timestamp": timestamp,
            "watermark_authentic": watermark_hash,
            "creator": "Syams Maulana (ICAM)",
            "protocol": "Al-Haqq Bimetallic Auction Standard"
        },
        "summary": {
            "total_items_listed": len(auction_items),
            "total_funds_raised_usd": f"${total_usd_raised:,.2f}",
            "total_equivalent_gold": f"{total_usd_raised / gold_spot_usd:.4f} Grams 24K Gold (ICAM-G)",
            "community_fund_allocation": "100% Peralatan Vokasi Kuliner & Ekspedisi Social"
        },
        "items": auction_items
    }

    with open("auction_status.json", "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"[SUCCESS] Auction Tracker Al-Haqq berhasil dieksekusi.")
    print(f"[TOTAL RAISED] ${total_usd_raised:,.2f} (~{total_usd_raised / gold_spot_usd:.2f} ICAM-G)")
    print(f"[WATERMARK] {watermark_hash}")

if __name__ == "__main__":
    run_auction_tracker()
