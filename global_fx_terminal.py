import urllib.request
import json
from datetime import datetime

def fetch_global_fx_status():
    print("=" * 65)
    print("🌍 AL-HAQQ GLOBAL FX & DEDUCTION MINIMIZATION TELEMETRY")
    print("=" * 65)
    print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Fetching live interbank exchange rates...\n")

    try:
        url = "https://api.frankfurter.app/latest?from=EUR"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        base = data.get("base", "EUR")
        rates = data.get("rates", {})
        
        # Target currencies of strategic interest
        tracked = ["USD", "GBP", "JPY", "IDR", "CHF", "CAD"]
        
        print(f"Base Currency: {base} (Optimized via Zero-Markup VCC Rail)\n")
        print(f"{'Currency':<10} | {'Exchange Rate':<15} | {'Est. Fee Overhead':<20}")
        print("-" * 53)
        
        for curr in tracked:
            if curr in rates:
                rate = rates[curr]
                # Assuming optimized VCC fee (e.g. Revolut/Wise weekday 0.5%) vs Traditional Web Gateway (3.5%)
                fee_overhead = "~0.5% (Interbank)" if curr in ["USD", "GBP", "CHF"] else "~1.2% (Cross-FX)"
                print(f"{curr:<10} | {rate:<15.4f} | {fee_overhead:<20}")
                
        print("-" * 53)
        print("💡 Optimization Verdict:")
        print(" • Route via Local Store + Multi-Currency VCC to eliminate Coda/Web surcharges.")
        print(" • Avoid weekend currency conversions where liquidity spreads widen by 0.5%–1.5%.")
        
    except Exception as e:
        print(f"❌ Error fetching live FX telemetry: {e}")
    print("=" * 65)

if __name__ == "__main__":
    fetch_global_fx_status()
