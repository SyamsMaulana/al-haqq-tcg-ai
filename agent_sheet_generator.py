









#!/usr/bin/env python3
"""
agent_sheet_generator.py — Generator Lembar Cetak Kartu Phygital & Karsa Agents
Integritas Al-Haqq Framework & Karsa Kreatif Kolektif
Inisiator & Pemikir Utama: ICAM / Syams Maulana (Node G.O.D)
"""

import os
import sys
import deck_data
import agent_data

def generate_print_sheet():
    filename = "al_haqq_card_sheet.html"
    
    html_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Al-Haqq Protocol TCG — Lembar Cetak Aset Phygital (63x88mm)</title>
    <style>
        body { 
            font-family: 'Helvetica Neue', Arial, sans-serif; 
            background-color: #e5e5e5; 
            color: #2c3e50; 
            margin: 0; 
            padding: 20px; 
        }
        .header { 
            text-align: center; 
            margin-bottom: 25px; 
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header h1 { margin: 0 0 8px 0; font-size: 1.5em; color: #1a252f; }
        .header p { margin: 0; font-size: 0.9em; color: #7f8c8d; }
        
        .sheet { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 15px; 
            justify-content: center; 
        }
        .card { 
            width: 63mm; 
            height: 88mm; 
            background: #ffffff; 
            border: 2px solid #2c3e50; 
            border-radius: 6px; 
            padding: 4mm; 
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        .card-agent { border-color: #27ae60; }
        
        .card-header { 
            font-weight: bold; 
            font-size: 8.5pt; 
            color: #1a252f; 
            border-bottom: 1px solid #bdc3c7; 
            padding-bottom: 4px; 
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .tag { 
            background: #2c3e50; 
            color: #fff; 
            padding: 2px 5px; 
            border-radius: 3px; 
            font-size: 6.5pt; 
            text-transform: uppercase;
        }
        .tag-agent { background: #27ae60; }
        
        .card-body { 
            font-size: 7.5pt; 
            margin: 4px 0; 
            line-height: 1.25; 
        }
        .stats { 
            font-size: 7.5pt; 
            font-weight: bold; 
            color: #2c3e50; 
            background: #f8f9fa; 
            padding: 4px; 
            border-radius: 3px; 
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .narrative {
            font-style: italic;
            font-size: 6.5pt;
            color: #555;
            text-align: center;
            margin: 2px 0;
        }
        .watermark { 
            font-size: 6pt; 
            color: #7f8c8d; 
            text-align: center; 
            border-top: 1px dashed #bdc3c7; 
            padding-top: 3px; 
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎴 Al-Haqq Protocol TCG — Lembar Cetak Resmi</h1>
        <p>Integritas Mizan, Karsa Agents, & Verifikasi Phygital | Cap Digital: ICAM / Syams Maulana</p>
    </div>
    
    <div class="sheet">
"""

    # Render Kartu Starter Deck
    for card in deck_data.starter_deck_database:
        html_content += f"""
        <div class="card">
            <div>
                <div class="card-header">
                    <span>{card['card_id']}</span>
                    <span class="tag">Starter</span>
                </div>
                <div class="card-body">
                    <strong>{card['name']}</strong><br>
                    <span style="color: #666; font-size: 7pt;">Kat: {card['category']}</span>
                </div>
            </div>
            <div>
                <div class="stats">
                    Casual (K): {card['casual_cost']} | Turbo (T): {card['turbo_cost']}
                </div>
                <div class="narrative">"{card['narrative']}"</div>
                <div class="watermark">Al-Haqq Protocol • ICAM / Syams Maulana</div>
            </div>
        </div>
        """

    # Render Karsa Agents
    for agent in agent_data.karsa_agents_database:
        html_content += f"""
        <div class="card card-agent">
            <div>
                <div class="card-header" style="border-color: #27ae60;">
                    <span>{agent['agent_id']}</span>
                    <span class="tag tag-agent">Agent</span>
                </div>
                <div class="card-body">
                    <strong>{agent['name']}</strong><br>
                    <span style="color: #666; font-size: 6.5pt;">{agent['ability']}</span>
                </div>
            </div>
            <div>
                <div class="stats" style="background: #f0fdf4; border-color: #bbf7d0;">
                    Inf: {agent['influence_power']} | Dur: {agent['durability']}
                </div>
                <div class="narrative">"{agent['narrative']}"</div>
                <div class="watermark">Al-Haqq Protocol • ICAM / Syams Maulana</div>
            </div>
        </div>
        """

    html_content += """
    </div>
</body>
</html>
"""

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[SUKSES] Lembar cetak HTML '{filename}' berhasil di-generate secara optimal (Standar TCG 63x88mm).")
    except Exception as e:
        print(f"[ERROR] Gagal menulis file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_print_sheet()
