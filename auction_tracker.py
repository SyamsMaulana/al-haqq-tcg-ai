import json
import datetime
import hashlib

def run_auction_tracker():
    timestamp = datetime.datetime.utcnow().isoformat()
    watermark_raw = f"ICAM-AUCTION-AL-HAQQ-{timestamp}"
    watermark_hash = f"ICAM-DIGITAL-WM-{hashlib.sha256(watermark_raw.encode()).hexdigest()[:12].upper()}"

    # Acuan Kurs Dasar (Rupiah First Pipeline)
    idr_per_usd = 16000.00          # 1 USD = Rp 16.000
    gold_idr_per_g = 1360000.00     # 1 Gram Emas 24K (1 ICAM-G) = Rp 1.360.000
    silver_idr_per_g = 16000.00     # 1 Gram Perak Murni (1 ICAM-S) = Rp 16.000

    auction_items = [
        {
            "id": "AUC-001",
            "item_name": "Hermès Koala Print Silk Tie",
            "highest_bid_idr": 3808000, # Base Wajib IDR (Setara ~$238.00)
            "bidder": "Collector_01",
            "target_allocation": "Commercial Pastry Mixer 10L Komunitas",
            "status": "Active Bidding"
        },
        {
            "id": "AUC-002",
            "item_name": "Max Raab American Flags Vintage Tie",
            "highest_bid_idr": 2040000, # Base Wajib IDR (Setara ~$127.50)
            "bidder": "Collector_07",
            "target_allocation": "Artisan Deck Oven & Pizza Stone Setup",
            "status": "Active Bidding"
        },
        {
            "id": "AUC-003",
            "item_name": "Goldlion 1500 Special Edition Tie",
            "highest_bid_idr": 1632000, # Base Wajib IDR (Setara ~$102.00)
            "bidder": "Collector_03",
            "target_allocation": "Set Pisau Chef & Talenan Vokasi",
            "status": "Active Bidding"
        },
        {
            "id": "AUC-004",
            "item_name": "Koleksi Memorabilia & Aksesori Vintage",
            "highest_bid_idr": 4760000, # Base Wajib IDR (Setara ~$297.50)
            "bidder": "Collector_09",
            "target_allocation": "Bahan Baku & Equipment Vokasi Kuliner",
            "status": "In Preparation"
        }
    ]

    total_idr_raised = 0.0
    for item in auction_items:
        bid_idr = item["highest_bid_idr"]
        total_idr_raised += bid_idr
        
        # Konversi Berjenjang: IDR -> USD -> ICAM Currency
        bid_usd = bid_idr / idr_per_usd
        icam_g = bid_idr / gold_idr_per_g
        icam_s = bid_idr / silver_idr_per_g

        item["highest_bid_formatted_idr"] = f"Rp {bid_idr:,.0f}".replace(",", ".")
        item["converted_usd"] = f"${bid_usd:,.2f}"
        item["icam_gold_value"] = f"{icam_g:.4f} ICAM-G"
        item["icam_silver_value"] = f"{icam_s:.2f} ICAM-S"

    total_usd_raised = total_idr_raised / idr_per_usd
    total_gold_grams = total_idr_raised / gold_idr_per_g

    log_data = {
        "metadata": {
            "timestamp": timestamp,
            "watermark_authentic": watermark_hash,
            "creator": "Syams Maulana (ICAM)",
            "protocol": "Al-Haqq IDR-First Bimetallic Auction Standard"
        },
        "rates_reference": {
            "idr_per_usd": f"Rp {idr_per_usd:,.0f}".replace(",", "."),
            "gold_24k_idr_per_gram": f"Rp {gold_idr_per_g:,.0f}".replace(",", "."),
            "silver_idr_per_gram": f"Rp {silver_idr_per_g:,.0f}".replace(",", ".")
        },
        "summary": {
            "total_items_listed": len(auction_items),
            "total_funds_raised_idr": f"Rp {total_idr_raised:,.0f}".replace(",", "."),
            "total_funds_raised_usd": f"${total_usd_raised:,.2f}",
            "total_equivalent_gold": f"{total_gold_grams:.4f} Grams 24K Gold (ICAM-G)",
            "community_fund_allocation": "100% Peralatan Vokasi Kuliner & Ekspedisi Social"
        },
        "items": auction_items
    }

    with open("auction_status.json", "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"[SUCCESS] Auction Tracker (IDR-First Architecture) berhasil dieksekusi.")
    print(f"[TOTAL RAISED IDR] Rp {total_idr_raised:,.0f}".replace(",", "."))
    print(f"[CONVERTED USD] ${total_usd_raised:,.2f}")
    print(f"[ICAM GOLD EQUIVALENT] {total_gold_grams:.4f} ICAM-G")
    print(f"[WATERMARK] {watermark_hash}")

if __name__ == "__main__":
    run_auction_tracker()
