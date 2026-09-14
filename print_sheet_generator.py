








import json
import deck_data

def generate_print_html():
    with open("phygital_payloads.json", "r", encoding="utf-8") as f:
        payloads = json.load(f)

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Al-Haqq TCG - Print Sheet (63x88mm)</title>
        <style>
            body { font-family: Arial, sans-serif; background: #e0e0e0; margin: 0; padding: 10px; }
            .sheet { display: flex; flex-wrap: wrap; gap: 8px; width: 210mm; margin: 0 auto; background: white; padding: 10mm; box-sizing: border-box; }
            .card { width: 63mm; height: 88mm; border: 1px dashed #666; padding: 4mm; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; font-size: 9pt; background: #fff; }
            .card-header { font-weight: bold; border-bottom: 1px solid #333; padding-bottom: 2mm; }
            .card-body { font-size: 8pt; margin: 2mm 0; line-height: 1.2; }
            .card-footer { font-size: 6.5pt; border-top: 1px solid #ccc; padding-top: 2mm; color: #444; }
            .tag { font-family: monospace; font-size: 5.5pt; background: #f4f4f4; padding: 2px; word-break: break-all; display: block; margin-top: 2px; }
        </style>
    </head>
    <body>
        <div class="sheet">
    """

    for card in deck_data.starter_deck_database:
        cid = card['card_id']
        payload = payloads.get(cid, {})
        html_content += f"""
            <div class="card">
                <div class="card-header">
                    {card['card_id']} — {card['name']}<br>
                    <span style="font-weight: normal; font-size: 7.5pt;">{card['category']}</span>
                </div>
                <div class="card-body">
                    <b>Mana:</b> K {card['casual_cost']} | T {card['turbo_cost']}<br><br>
                    <b>Efek:</b> {card['effect']}<br><br>
                    <i style="font-size: 7pt;">"{card['narrative']}"</i>
                </div>
                <div class="card-footer">
                    <b>Phygital Verification Token:</b>
                    <span class="tag">{payload.get('verification_hash', '')}</span>
                </div>
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    with open("print_sheet.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Lembar cetak 'print_sheet.html' berhasil dibuat sesuai dimensi standar kartu 63x88mm.")

if __name__ == "__main__":
    generate_print_html()

