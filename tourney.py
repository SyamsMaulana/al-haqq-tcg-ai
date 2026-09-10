import json
from datetime import datetime

def generate_tournament_log():
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "command_issuer": "GOD•MauL (ICAM)",
        "distributions": {
            "referee_aninkz": {
                "reward": "2x Booster Pack Terbaru",
                "condition": "Claim after match report completion"
            },
            "team_blackrose": {
                "reward": "1x Booster Pack per member",
                "condition": "Guaranteed win or loss (Appreciation for serious play & respect)"
            },
            "roster_takmaul": {
                "status": "Active Team Wars participant lineup"
            }
        },
        "framework_principle": "Al-Haqq & Piramida Terbalik - Autentik & Adil"
    }

    file_name = f"tourney_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)
        
    print(f"[OK] Log turnamen berhasil di-generate dan diamankan di: {file_name}")

if __name__ == "__main__":
    generate_tournament_log()
