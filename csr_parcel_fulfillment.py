

import json

class CSRParcelFulfillment:
    def __init__(self):
        self.item_specs = {
            "booster_pack_per_nomination": 50,
            "guarantee_tier_rarity_per_booster": 1,
            "sleeves_per_pack": 300
        }

    def calculate_top10_verified_reward(self, company_name, registered_nominations, payment_verified=True):
        if not payment_verified:
            return {"error": "Payment not verified. Free sleeves benefit requires completed verification."}
        
        # 1 Executive Box per nominasi + 1 Free Exclusive Sleeves pack (300 pcs) per nominasi
        total_boxes = registered_nominations
        total_boosters = total_boxes * self.item_specs["booster_pack_per_nomination"]
        free_sleeves_packs = registered_nominations # 1 pack per nominasi
        total_sleeves_pcs = free_sleeves_packs * self.item_specs["sleeves_per_pack"]
        
        manifest = {
            "company_target": company_name,
            "tier_status": "Top 10 Verified Paid Company",
            "payment_verification": "SUCCESS",
            "registered_nominations": registered_nominations,
            "allocation_details": {
                "executive_boxes": total_boxes,
                "booster_packs_total": total_boosters,
                "per_booster_guarantee": f"{self.item_specs['guarantee_tier_rarity_per_booster']} Tier Rarity Card",
                "free_exclusive_sleeves_packs": free_sleeves_packs,
                "free_sleeves_total_pcs": total_sleeves_pcs
            },
            "backend_validation": "Validated by Meprindo Media Group & Tech Master Tracking"
        }
        
        filename = f"top10_verified_{company_name.lower().replace(' ', '_')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        print(f"[TOP 10 MANIFEST] Paket terverifikasi untuk {company_name} berhasil disimpan ke {filename}")

if __name__ == "__main__":
    fulfillment = CSRParcelFulfillment()
    
    # Contoh Simulasi untuk Perusahaan Top 10 yang sudah bayar (Misal mendaftarkan 2 nominasi)
    fulfillment.calculate_top10_verified_reward(
        company_name="PT Nusantara Lestari Energi", 
        registered_nominations=2, 
        payment_verified=True
    )


import json

class CSRParcelFulfillment:
    def __init__(self):
        self.item_specs = {
            "booster_pack_per_nomination": 50,
            "guarantee_tier_rarity_per_booster": 1,
            "sleeves_per_pack": 300
        }

    def calculate_participant_reward(self, years_participated, nominations_per_year):
        total_nominations = years_participated * nominations_per_year
        total_boxes = total_nominations 
        total_boosters = total_boxes * self.item_specs["booster_pack_per_nomination"]

        return {
            "years_active": years_participated,
            "nominations_per_year": nominations_per_year,
            "total_executive_boxes": total_boxes,
            "total_booster_packs": total_boosters,
            "per_booster_guarantee": f"{self.item_specs['guarantee_tier_rarity_per_booster']} Tier Rarity Card"
        }

    def calculate_sponsor_reward(self, tier):
        tier_data = tier.lower()
        if tier_data == "gold":
            return {"tier": "Gold Sponsor", "executive_boxes": 3, "executive_sleeves_packs": 3, "sleeves_total_pcs": 3 * self.item_specs["sleeves_per_pack"]}
        elif tier_data == "silver":
            return {"tier": "Silver Sponsor", "executive_boxes": 2, "executive_sleeves_packs": 2, "sleeves_total_pcs": 2 * self.item_specs["sleeves_per_pack"]}
        elif tier_data == "bronze":
            return {"tier": "Bronze Sponsor", "executive_boxes": 1, "executive_sleeves_packs": 1, "sleeves_total_pcs": 1 * self.item_specs["sleeves_per_pack"]}
        return None

    def generate_parcel_manifest(self, company_name, category_type, data_input):
        manifest = {
            "company_target": company_name,
            "parcel_category": category_type,
            "allocation_details": data_input,
            "special_edition_specs": {
                "item": "Special Edition C-Series Executive Sleeves",
                "quantity_per_pack": f"{self.item_specs['sleeves_per_pack']} pcs"
            },
            "backend_validation": "Validated by Meprindo Media Group & Tech Master Tracking"
        }

        filename = f"parcel_manifest_{company_name.lower().replace(' ', '_')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        print(f"[MANIFEST GENERATED] Berhasil menyusun paket parcel untuk {company_name} -> Disimpan ke {filename}")

if __name__ == "__main__":
    fulfillment = CSRParcelFulfillment()
    participant_sim = fulfillment.calculate_participant_reward(years_participated=5, nominations_per_year=2)
    fulfillment.generate_parcel_manifest("PT Teladan Lestari", "Loyal Participant Tier", participant_sim)

    sponsor_sim = fulfillment.calculate_sponsor_reward("gold")
    fulfillment.generate_parcel_manifest("PT Mitra Nusantara Utama", "Gold Sponsor Tier", sponsor_sim)
