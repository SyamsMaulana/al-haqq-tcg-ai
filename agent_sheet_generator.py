








import json
import agent_data

def generate_agent_print_html():
    agents = agent_data.karsa_agents_database

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Al-Haqq TCG - Karsa Agents Print Sheet (63x88mm)</title>
        <style>
            body { font-family: Arial, sans-serif; background: #e0e0e0; margin: 0; padding: 10px; }
            .sheet { display: flex; flex-wrap: wrap; gap: 8px; width: 210mm; margin: 0 auto; background: white; padding: 10mm; box-sizing: border-box; }
            .card { width: 63mm; height: 88mm; border: 1px dashed #666; padding: 4mm; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; font-size: 9pt; background: #fdfdfd; }
            .card-header { font-weight: bold; border-bottom: 1px solid #333; padding-bottom: 2mm; }
            .card-body { font-size: 8pt; margin: 2mm 0; line-height: 1.2; }
            .card-footer { font-size: 6.5pt; border-top: 1px solid #ccc; padding-top: 2mm; color: #444; }
            .stats { font-weight: bold; color: #111; background: #eee; padding: 2px 4px; border-radius: 3px; display: inline-block; margin-top: 2px; }
        </style>
    </head>
    <body>
        <div class="sheet">
    """

    for agent in agents:
        html_content += f"""
            <div class="card">
                <div class="card-header">
                    {agent['agent_id']} — {agent['name']}<br>
                    <span style="font-weight: normal; font-size: 7.5pt; color: #555;">{agent['category']}</span>
                </div>
                <div class="card-body">
                    <b>Mana:</b> K {agent['casual_cost']} | T {agent['turbo_cost']}<br>
                    <div class="stats">Inf: {agent['influence_power']} | Dur: {agent['durability']}</div><br>
                    <b>Ability:</b> {agent['ability']}<br><br>
                    <i style="font-size: 7pt;">"{agent['narrative']}"</i>
                </div>
                <div class="card-footer">
                    <b>Phygital Agent Node:</b> ALHAQQ-AGENT-{agent['agent_id']}-2026
                </div>
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    with open("print_sheet_agents.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Lembar cetak agen 'print_sheet_agents.html' berhasil dibuat sesuai dimensi standar kartu 63x88mm.")

if __name__ == "__main__":
    generate_agent_print_html()
