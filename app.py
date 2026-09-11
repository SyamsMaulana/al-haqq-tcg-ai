from flask import Flask, render_template_string, request, jsonify, Response
import datetime
import sqlite3
import random
import json
import math
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            strategy TEXT,
            main_cards TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_name TEXT,
            opponent TEXT,
            result TEXT,
            notes TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            points INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            effect TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matchups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archetype TEXT,
            counter_strategy TEXT,
            sideboard_tips TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sideboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            archetype TEXT,
            cards_in TEXT,
            cards_out TEXT,
            notes TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_name TEXT,
            hand_cards TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_name TEXT,
            rarity TEXT,
            condition TEXT,
            qty INTEGER,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_name TEXT,
            target_price TEXT,
            priority TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_partner TEXT,
            cards_given TEXT,
            cards_received TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_name TEXT,
            price TEXT,
            source TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hypergeometric(k, N, K, n):
    try:
        def comb(n, r):
            if r < 0 or r > n:
                return 0
            return math.comb(n, r)
        prob = (comb(K, k) * comb(N - K, n - k)) / comb(N, n)
        return prob
    except Exception:
        return 0.0

def parse_price(price_str):
    if not price_str:
        return 0
    clean = re.sub(r'[^0-9]', '', str(price_str))
    try:
        return int(clean) if clean else 0
    except ValueError:
        return 0

HTML_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Al-Haqq TCG AI | GOD•MauL Hub v3.14</title>
    <style>
        :root {
            --bg: #0b0f19; --panel: #1e293b; --accent: #d97706; --text: #f8fafc; --console-bg: #090d16; --console-text: #4ade80;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 1.25rem; display: flex; flex-direction: column; min-height: 100vh; gap: 1rem; }
        .container { max-width: 900px; width: 100%; margin: 0 auto; display: flex; flex-direction: column; gap: 1rem; flex: 1; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem; }
        .header h1 { font-size: 1.4rem; color: var(--accent); }
        .badge-group { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
        .badge, .btn-export { background: var(--accent); color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; text-decoration: none; border: none; cursor: pointer; }
        .badge-val { background: #10b981; }
        .btn-export { background: #0ea5e9; }
        .btn-md { background: #10b981; }
        .console-box { background: var(--console-bg); color: var(--console-text); font-family: monospace; padding: 1rem; border-radius: 8px; height: 180px; overflow-y: auto; border: 1px solid #334155; white-space: pre-wrap; font-size: 0.8rem; }
        .input-group { display: flex; gap: 0.5rem; }
        input[type="text"] { flex: 1; padding: 0.7rem; background: var(--panel); border: 1px solid #475569; color: white; border-radius: 6px; font-size: 1rem; }
        input[type="text"]:focus { outline: none; border-color: var(--accent); }
        button.send-btn { background: var(--accent); color: white; border: none; padding: 0 1.25rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
        .table-card { background: var(--panel); border-radius: 8px; padding: 1rem; border: 1px solid #334155; }
        .table-card h2 { font-size: 0.95rem; color: var(--accent); margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; }
        table { width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left; }
        th, td { padding: 0.5rem; border-bottom: 1px solid #334155; }
        th { color: #94a3b8; }
        footer { text-align: center; font-size: 0.75rem; color: #64748b; border-top: 1px solid #1e293b; padding-top: 0.75rem; margin-top: auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Al-Haqq TCG AI</h1>
            <div class="badge-group">
                <div id="totalValBadge" class="badge badge-val">Total Valuasi: Rp 0</div>
                <a href="/api/export/md" class="btn-export btn-md" target="_blank">Ekspor Markdown</a>
                <a href="/api/export" class="btn-export" target="_blank">Ekspor JSON</a>
                <div class="badge">GOD•MauL Hub v3.14</div>
            </div>
        </div>
        <div id="console" class="console-box">[System] Al-Haqq Protocol & Engine v3.14 Active (Portfolio & Net Worth Vault Loaded).
[AI] Perintah Tersedia:
 - 'portfolio' -> Cek total estimasi nilai koleksi inventory
 - 'price add [nama kartu] | [harga pasar] | [sumber]'
 - 'trade add [partner] | [cards given] | [cards received] | [status]'
 - 'want add [nama kartu] | [target harga] | [prioritas]'
 - 'inv add [nama kartu] | [rarity] | [kondisi] | [jumlah]'
 - 'draw [nama deck]' -> Simulasi buka 5 kartu awal
 - 'deck [nama deck] | [strategi] | [kartu utama]'
 - 'sideboard [archetype] | [cards in] | [cards out] | [catatan]'
 - 'log match [deck] vs [opponent] | [WIN/LOSS] | [catatan]'
 - 'add card [nama] | [kategori] | [efek]'
 - 'prob [deck] | [copies] | [hand] | [target_min]'
 - 'score match [player1] vs [player2] | [pemenang]'
 - 'register [nama player]' | 'standings' | 'pairings'</div>
        <div class="input-group">
            <input type="text" id="commandInput" placeholder="Ketik cth: portfolio atau price add Ash Blossom | Rp 75.000 | Store" autocomplete="off">
            <button class="send-btn" onclick="sendCommand()">Kirim</button>
        </div>
        <div class="table-card">
            <h2>Market & Valuation Vault (GOD•MauL Price Tracker)</h2>
            <table>
                <thead><tr><th>Nama Kartu</th><th>Harga Pasar</th><th>Sumber / Marketplace</th><th>Waktu Update</th></tr></thead>
                <tbody id="priceTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Trade & Binder Vault (GOD•MauL Local Trades)</h2>
            <table>
                <thead><tr><th>Partner Trade</th><th>Kartu Diberikan (- Give)</th><th>Kartu Diterima (+ Receive)</th><th>Status</th><th>Waktu</th></tr></thead>
                <tbody id="tradeTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Wants List & Target Vault (GOD•MauL Wishlist)</h2>
            <table>
                <thead><tr><th>Nama Kartu Buruan</th><th>Target Harga</th><th>Prioritas</th><th>Waktu Input</th></tr></thead>
                <tbody id="wantTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Inventory Vault & Collection Tracker (GOD•MauL Collection)</h2>
            <table>
                <thead><tr><th>Nama Kartu</th><th>Rarity</th><th>Kondisi</th><th>Jumlah (Qty)</th></tr></thead>
                <tbody id="invTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Hand Simulator Vault (GOD•MauL Opening Hand Test)</h2>
            <table>
                <thead><tr><th>Deck Simulasi</th><th>Komposisi Starting Hand (5 Kartu)</th><th>Waktu</th></tr></thead>
                <tbody id="simTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Deck Builder Vault (GOD•MauL Composition)</h2>
            <table>
                <thead><tr><th>Nama Deck</th><th>Strategi Utama</th><th>Komposisi Kartu Inti</th></tr></thead>
                <tbody id="deckTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Sideboard Matrix & Matchup Optimizer (GOD•MauL Tactics)</h2>
            <table>
                <thead><tr><th>Archetype Lawan</th><th>Cards IN (+ Sideboard)</th><th>Cards OUT (- Main)</th><th>Catatan Strategi</th></tr></thead>
                <tbody id="sideboardTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Riwayat Pertandingan & Win-Rate (GOD•MauL Analytics)</h2>
            <table>
                <thead><tr><th>Deck Kamu</th><th>Lawan</th><th>Hasil</th><th>Catatan / Evaluasi</th></tr></thead>
                <tbody id="matchTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Basis Data Kartu TCG (GOD•MauL Archive)</h2>
            <table>
                <thead><tr><th>Nama Kartu</th><th>Kategori</th><th>Efek / Keterangan</th></tr></thead>
                <tbody id="cardTableBody"></tbody>
            </table>
        </div>
        <div class="table-card">
            <h2>Klasemen Turnamen Swiss (GOD•Community Auto-Standings)</h2>
            <table>
                <thead><tr><th>Rank</th><th>Player</th><th>Poin</th><th>W / L</th></tr></thead>
                <tbody id="playerTableBody"></tbody>
            </table>
        </div>
        <footer>Digital Watermark & Signature (ICAM / Syams Maulana & Al-Haqq Protocol): Cap digital kolaborasi pemikiran dan penyempurnaan bersama.</footer>
    </div>
    <script>
        async function fetchData() {
            try {
                const resPort = await fetch('/api/portfolio/summary');
                const portData = await resPort.json();
                document.getElementById('totalValBadge').innerText = `Total Valuasi: ${portData.formatted_total}`;

                const resPrice = await fetch('/api/prices');
                const prices = await resPrice.json();
                const tbodyPrice = document.getElementById('priceTableBody');
                tbodyPrice.innerHTML = prices.length === 0 ? '<tr><td colspan="4" style="text-align:center; color:#64748b;">Belum ada data harga pasar. Gunakan: price add [nama] | [harga] | [sumber]</td></tr>' : '';
                prices.forEach(p => {
                    tbodyPrice.innerHTML += `<tr><td><strong>${p.card_name}</strong></td><td><span style="color:#4ade80; font-weight:bold;">${p.price}</span></td><td><span style="color:#38bdf8">${p.source}</span></td><td>${p.timestamp}</td></tr>`;
                });

                const resTrade = await fetch('/api/trades');
                const trades = await resTrade.json();
                const tbodyTrade = document.getElementById('tradeTableBody');
                tbodyTrade.innerHTML = trades.length === 0 ? '<tr><td colspan="5" style="text-align:center; color:#64748b;">Belum ada riwayat trade.</td></tr>' : '';
                trades.forEach(t => {
                    const stColor = t.status.toLowerCase() === 'completed' ? '#4ade80' : (t.status.toLowerCase() === 'cancelled' ? '#f87171' : '#facc15');
                    tbodyTrade.innerHTML += `<tr><td><strong>${t.trade_partner}</strong></td><td><span style="color:#f87171">${t.cards_given}</span></td><td><span style="color:#4ade80">${t.cards_received}</span></td><td><span style="color:${stColor}; font-weight:bold;">${t.status}</span></td><td>${t.timestamp}</td></tr>`;
                });

                const resWant = await fetch('/api/wants');
                const wants = await resWant.json();
                const tbodyWant = document.getElementById('wantTableBody');
                tbodyWant.innerHTML = wants.length === 0 ? '<tr><td colspan="4" style="text-align:center; color:#64748b;">Belum ada wants list.</td></tr>' : '';
                wants.forEach(w => {
                    const pColor = w.priority.toLowerCase() === 'high' ? '#f87171' : (w.priority.toLowerCase() === 'med' ? '#facc15' : '#4ade80');
                    tbodyWant.innerHTML += `<tr><td><strong>${w.card_name}</strong></td><td><span style="color:#38bdf8">${w.target_price}</span></td><td><span style="color:${pColor}; font-weight:bold;">${w.priority}</span></td><td>${w.timestamp}</td></tr>`;
                });

                const resInv = await fetch('/api/inventory');
                const inv = await resInv.json();
                const tbodyInv = document.getElementById('invTableBody');
                tbodyInv.innerHTML = inv.length === 0 ? '<tr><td colspan="4" style="text-align:center; color:#64748b;">Belum ada inventaris kartu.</td></tr>' : '';
                inv.forEach(i => {
                    tbodyInv.innerHTML += `<tr><td><strong>${i.card_name}</strong></td><td><span style="color:#facc15">${i.rarity}</span></td><td>${i.condition}</td><td><span style="color:#4ade80; font-weight:bold;">x${i.qty}</span></td></tr>`;
                });

                const resSims = await fetch('/api/simulations');
                const sims = await resSims.json();
                const tbodySim = document.getElementById('simTableBody');
                tbodySim.innerHTML = sims.length === 0 ? '<tr><td colspan="3" style="text-align:center; color:#64748b;">Belum ada simulasi hand.</td></tr>' : '';
                sims.forEach(s => {
                    tbodySim.innerHTML += `<tr><td><strong>${s.deck_name}</strong></td><td><span style="color:#4ade80">${s.hand_cards}</span></td><td>${s.timestamp}</td></tr>`;
                });

                const resDecks = await fetch('/api/decks');
                const decks = await resDecks.json();
                const tbodyD = document.getElementById('deckTableBody');
                tbodyD.innerHTML = decks.length === 0 ? '<tr><td colspan="3" style="text-align:center; color:#64748b;">Belum ada deck tersimpan.</td></tr>' : '';
                decks.forEach(d => {
                    tbodyD.innerHTML += `<tr><td><strong>${d.name}</strong></td><td><span style="color:#38bdf8">${d.strategy}</span></td><td>${d.main_cards}</td></tr>`;
                });

                const resSb = await fetch('/api/sideboards');
                const sideboards = await resSb.json();
                const tbodySb = document.getElementById('sideboardTableBody');
                tbodySb.innerHTML = sideboards.length === 0 ? '<tr><td colspan="4" style="text-align:center; color:#64748b;">Belum ada data sideboard.</td></tr>' : '';
                sideboards.forEach(s => {
                    tbodySb.innerHTML += `<tr><td><strong>${s.archetype}</strong></td><td><span style="color:#4ade80">${s.cards_in}</span></td><td><span style="color:#f87171">${s.cards_out}</span></td><td>${s.notes}</td></tr>`;
                });

                const resMatches = await fetch('/api/matches');
                const matches = await resMatches.json();
                const tbodyM = document.getElementById('matchTableBody');
                tbodyM.innerHTML = matches.length === 0 ? '<tr><td colspan="4" style="text-align:center; color:#64748b;">Belum ada riwayat match.</td></tr>' : '';
                matches.forEach(m => {
                    const resColor = m.result.toUpperCase() === 'WIN' ? '#4ade80' : '#f87171';
                    tbodyM.innerHTML += `<tr><td><strong>${m.deck_name}</strong></td><td>${m.opponent}</td><td><span style="color:${resColor}; font-weight:bold;">${m.result.toUpperCase()}</span></td><td>${m.notes}</td></tr>`;
                });

                const resCards = await fetch('/api/cards');
                const cards = await resCards.json();
                const tbodyC = document.getElementById('cardTableBody');
                tbodyC.innerHTML = cards.length === 0 ? '<tr><td colspan="3" style="text-align:center; color:#64748b;">Belum ada kartu tersimpan.</td></tr>' : '';
                cards.forEach(c => {
                    tbodyC.innerHTML += `<tr><td><strong>${c.name}</strong></td><td><span style="color:#38bdf8">${c.category}</span></td><td>${c.effect}</td></tr>`;
                });

                const resPlayers = await fetch('/api/players');
                const players = await resPlayers.json();
                const tbodyP = document.getElementById('playerTableBody');
                tbodyP.innerHTML = players.length === 0 ? '<tr><td colspan="4" style="text-align:center; color:#64748b;">Belum ada peserta terdaftar.</td></tr>' : '';
                players.forEach((p, index) => {
                    tbodyP.innerHTML += `<tr><td>#${index+1}</td><td><strong>${p.name}</strong></td><td><span style="color:#facc15; font-weight:bold;">${p.points} PTS</span></td><td><span style="color:#4ade80">${p.wins}W</span> / <span style="color:#f87171">${p.losses}L</span></td></tr>`;
                });
            } catch (e) {}
        }
        async function sendCommand() {
            const input = document.getElementById('commandInput');
            const consoleBox = document.getElementById('console');
            const cmd = input.value.trim();
            if (!cmd) return;
            consoleBox.innerText += "\\n> " + cmd + "\\n[Processing...]";
            input.value = '';
            consoleBox.scrollTop = consoleBox.scrollHeight;
            try {
                const res = await fetch('/api/command', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({command: cmd}) });
                const data = await res.json();
                consoleBox.innerText = consoleBox.innerText.replace('[Processing...]', data.reply);
                fetchData();
            } catch (e) {
                consoleBox.innerText = consoleBox.innerText.replace('[Processing...]', '[Error] Koneksi gagal.');
            }
            consoleBox.scrollTop = consoleBox.scrollHeight;
        }
        document.getElementById('commandInput').addEventListener('keypress', e => { if (e.key === 'Enter') sendCommand(); });
        fetchData();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/api/prices', methods=['GET'])
def api_prices():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT card_name, price, source, timestamp FROM market_prices ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"card_name": r[0], "price": r[1], "source": r[2], "timestamp": r[3]} for r in rows])

@app.route('/api/portfolio/summary', methods=['GET'])
def api_portfolio_summary():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    # Fetch latest price for each card name
    cursor.execute("SELECT card_name, price FROM market_prices")
    price_rows = cursor.fetchall()
    price_map = {}
    for cname, p_str in price_rows:
        price_map[cname.lower().strip()] = parse_price(p_str)

    cursor.execute("SELECT card_name, qty FROM inventory")
    inv_rows = cursor.fetchall()
    total_val = 0
    item_count = 0
    for cname, qty in inv_rows:
        key = cname.lower().strip()
        unit_price = price_map.get(key, 0)
        total_val += unit_price * (qty if qty else 1)
        item_count += (qty if qty else 1)
    conn.close()

    formatted_total = f"Rp {total_val:,}".replace(",", ".")
    return jsonify({"total_value": total_val, "formatted_total": formatted_total, "item_count": item_count})

@app.route('/api/trades', methods=['GET'])
def api_trades():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT trade_partner, cards_given, cards_received, status, timestamp FROM trades ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"trade_partner": r[0], "cards_given": r[1], "cards_received": r[2], "status": r[3], "timestamp": r[4]} for r in rows])

@app.route('/api/wants', methods=['GET'])
def api_wants():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT card_name, target_price, priority, timestamp FROM wants ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"card_name": r[0], "target_price": r[1], "priority": r[2], "timestamp": r[3]} for r in rows])

@app.route('/api/inventory', methods=['GET'])
def api_inventory():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT card_name, rarity, condition, qty, timestamp FROM inventory ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"card_name": r[0], "rarity": r[1], "condition": r[2], "qty": r[3], "timestamp": r[4]} for r in rows])

@app.route('/api/simulations', methods=['GET'])
def api_simulations():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT deck_name, hand_cards, timestamp FROM simulations ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"deck_name": r[0], "hand_cards": r[1], "timestamp": r[2]} for r in rows])

@app.route('/api/decks', methods=['GET'])
def api_decks():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, strategy, main_cards, timestamp FROM decks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"name": r[0], "strategy": r[1], "main_cards": r[2], "timestamp": r[3]} for r in rows])

@app.route('/api/sideboards', methods=['GET'])
def api_sideboards():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT archetype, cards_in, cards_out, notes, timestamp FROM sideboards ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"archetype": r[0], "cards_in": r[1], "cards_out": r[2], "notes": r[3], "timestamp": r[4]} for r in rows])

@app.route('/api/matches', methods=['GET'])
def api_matches():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT deck_name, opponent, result, notes, timestamp FROM matches ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"deck_name": r[0], "opponent": r[1], "result": r[2], "notes": r[3], "timestamp": r[4]} for r in rows])

@app.route('/api/cards', methods=['GET'])
def api_cards():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, effect, timestamp FROM cards ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"name": r[0], "category": r[1], "effect": r[2], "timestamp": r[3]} for r in rows])

@app.route('/api/players', methods=['GET'])
def api_players():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, points, wins, losses FROM players ORDER BY points DESC, wins DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"name": r[0], "points": r[1], "wins": r[2], "losses": r[3]} for r in rows])

@app.route('/api/export', methods=['GET'])
def api_export():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, card_name, price, source FROM market_prices ORDER BY id DESC")
    prices = [{"id": r[0], "card_name": r[1], "price": r[2], "source": r[3]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, trade_partner, cards_given, cards_received, status FROM trades ORDER BY id DESC")
    trades = [{"id": r[0], "trade_partner": r[1], "cards_given": r[2], "cards_received": r[3], "status": r[4]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, card_name, target_price, priority FROM wants ORDER BY id DESC")
    wants = [{"id": r[0], "card_name": r[1], "target_price": r[2], "priority": r[3]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, card_name, rarity, condition, qty FROM inventory ORDER BY id DESC")
    inventory = [{"id": r[0], "card_name": r[1], "rarity": r[2], "condition": r[3], "qty": r[4]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, deck_name, hand_cards FROM simulations ORDER BY id DESC")
    sims = [{"id": r[0], "deck_name": r[1], "hand_cards": r[2]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, name, strategy, main_cards FROM decks ORDER BY id DESC")
    decks = [{"id": r[0], "name": r[1], "strategy": r[2], "main_cards": r[3]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, archetype, cards_in, cards_out, notes FROM sideboards ORDER BY id DESC")
    sideboards = [{"id": r[0], "archetype": r[1], "cards_in": r[2], "cards_out": r[3], "notes": r[4]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, deck_name, opponent, result, notes FROM matches ORDER BY id DESC")
    matches = [{"id": r[0], "deck_name": r[1], "opponent": r[2], "result": r[3], "notes": r[4]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, name, category, effect FROM cards ORDER BY id DESC")
    cards = [{"id": r[0], "name": r[1], "category": r[2], "effect": r[3]} for r in cursor.fetchall()]
    cursor.execute("SELECT id, name, points, wins, losses FROM players ORDER BY points DESC")
    players = [{"id": r[0], "name": r[1], "points": r[2], "wins": r[3], "losses": r[4]} for r in cursor.fetchall()]
    conn.close()
    data = {"watermark": "Al-Haqq Protocol & ICAM / Syams Maulana Collaboration", "prices": prices, "trades": trades, "wants": wants, "inventory": inventory, "simulations": sims, "decks": decks, "sideboards": sideboards, "matches": matches, "cards": cards, "players": players}
    return Response(json.dumps(data, indent=4, ensure_ascii=False), mimetype="application/json", headers={"Content-Disposition": "attachment;filename=al_haqq_hub_v314_export.json"})

@app.route('/api/export/md', methods=['GET'])
def api_export_md():
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT card_name, price, source FROM market_prices ORDER BY id DESC")
    prices = cursor.fetchall()
    cursor.execute("SELECT trade_partner, cards_given, cards_received, status FROM trades ORDER BY id DESC")
    trades = cursor.fetchall()
    cursor.execute("SELECT card_name, target_price, priority FROM wants ORDER BY id DESC")
    wants = cursor.fetchall()
    cursor.execute("SELECT card_name, rarity, condition, qty FROM inventory ORDER BY id DESC")
    inventory = cursor.fetchall()
    cursor.execute("SELECT deck_name, hand_cards FROM simulations ORDER BY id DESC")
    sims = cursor.fetchall()
    cursor.execute("SELECT name, strategy, main_cards FROM decks ORDER BY id DESC")
    decks = cursor.fetchall()
    cursor.execute("SELECT archetype, cards_in, cards_out, notes FROM sideboards ORDER BY id DESC")
    sideboards = cursor.fetchall()
    cursor.execute("SELECT deck_name, opponent, result, notes FROM matches ORDER BY id DESC")
    matches = cursor.fetchall()
    cursor.execute("SELECT name, category, effect FROM cards ORDER BY id DESC")
    cards = cursor.fetchall()
    cursor.execute("SELECT name, points, wins, losses FROM players ORDER BY points DESC")
    players = cursor.fetchall()
    conn.close()

    lines = [
        "# AL-HAQQ TCG AI | GOD•MAUL HUB V3.14 ARCHIVE",
        "> **Digital Watermark & Copyright Protection (Al-Haqq Protocol / ICAM - Syams Maulana):** Cap digital kolaborasi pemikiran dan penyempurnaan bersama.",
        "",
        "## Market & Valuation Vault",
        "| Nama Kartu | Harga Pasar | Sumber / Marketplace |",
        "| :--- | :--- | :--- |"
    ]
    for p in prices:
        lines.append(f"| **{p[0]}** | {p[1]} | {p[2]} |")

    lines.extend([
        "",
        "## Trade & Binder Vault",
        "| Partner Trade | Kartu Diberikan (- Give) | Kartu Diterima (+ Receive) | Status |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for t in trades:
        lines.append(f"| **{t[0]}** | {t[1]} | {t[2]} | {t[3]} |")

    lines.extend([
        "",
        "## Wants List & Target Vault",
        "| Nama Kartu Buruan | Target Harga | Prioritas |",
        "| :--- | :--- | :--- |"
    ])
    for w in wants:
        lines.append(f"| **{w[0]}** | {w[1]} | {w[2]} |")

    lines.extend([
        "",
        "## Inventory Vault & Collection",
        "| Nama Kartu | Rarity | Kondisi | Jumlah (Qty) |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for i in inventory:
        lines.append(f"| **{i[0]}** | {i[1]} | {i[2]} | x{i[3]} |")

    lines.extend([
        "",
        "## Hand Simulator Vault",
        "| Deck Simulasi | Komposisi Starting Hand |",
        "| :--- | :--- |"
    ])
    for s in sims:
        lines.append(f"| **{s[0]}** | {s[1]} |")

    lines.extend([
        "",
        "## Deck Builder Vault",
        "| Nama Deck | Strategi Utama | Komposisi Kartu Inti |",
        "| :--- | :--- | :--- |"
    ])
    for d in decks:
        lines.append(f"| **{d[0]}** | {d[1]} | {d[2]} |")

    lines.extend([
        "",
        "## Sideboard Matrix & Matchup Optimizer",
        "| Archetype Lawan | Cards IN | Cards OUT | Catatan Strategi |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for s in sideboards:
        lines.append(f"| **{s[0]}** | {s[1]} | {s[2]} | {s[3]} |")

    lines.extend([
        "",
        "## Riwayat Pertandingan (Match History)",
        "| Deck Kamu | Lawan | Hasil | Catatan |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for m in matches:
        lines.append(f"| **{m[0]}** | {m[1]} | **{m[2]}** | {m[3]} |")

    lines.extend([
        "",
        "## Basis Data Kartu TCG",
        "| Nama Kartu | Kategori | Efek / Keterangan |",
        "| :--- | :--- | :--- |"
    ])
    for c in cards:
        lines.append(f"| **{c[0]}** | {c[1]} | {c[2]} |")
    
    lines.extend([
        "",
        "## Klasemen Turnamen Swiss",
        "| Rank | Player | Poin | Win / Lose |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for idx, p in enumerate(players):
        lines.append(f"| #{idx+1} | **{p[0]}** | {p[1]} PTS | {p[2]}W / {p[3]}L |")

    lines.extend([
        "",
        "---",
        "*Dokumen otomatis dari Al-Haqq Engine v3.14 (ICAM / Syams Maulana).*"
    ])
    
    return Response("\n".join(lines), mimetype="text/markdown", headers={"Content-Disposition": "attachment;filename=al_haqq_v314_archive.md"})

@app.route('/api/command', methods=['POST'])
def api_command():
    data = request.get_json()
    cmd = data.get('command', '').strip()
    cmd_l = cmd.lower()
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    conn = sqlite3.connect('god_maul_hub.db')
    cursor = conn.cursor()
    try:
        if cmd_l == "portfolio":
            cursor.execute("SELECT card_name, price FROM market_prices")
            price_map = {r[0].lower().strip(): parse_price(r[1]) for r in cursor.fetchall()}
            cursor.execute("SELECT card_name, qty FROM inventory")
            total_val = sum(price_map.get(r[0].lower().strip(), 0) * (r[1] if r[1] else 1) for r in cursor.fetchall())
            formatted_total = f"Rp {total_val:,}".replace(",", ".")
            reply = f"[{ts}] Portfolio Net Worth Vault:\\n• Total Estimasi Nilai Koleksi: {formatted_total}"
        elif cmd_l.startswith("price add "):
            content = cmd[10:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                cname = parts[0]
                price = parts[1] if len(parts) > 1 else "Rp 0"
                source = parts[2] if len(parts) > 2 else "Market"
                cursor.execute("INSERT INTO market_prices (card_name, price, source, timestamp) VALUES (?, ?, ?, ?)", (cname, price, source, ts))
                conn.commit()
                reply = f"[{ts}] Harga Pasar ditambahkan: '{cname}' [{price} via {source}]"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'price add [nama kartu] | [harga pasar] | [sumber]'"
        elif cmd_l.startswith("trade add "):
            content = cmd[10:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                partner = parts[0]
                given = parts[1] if len(parts) > 1 else "-"
                received = parts[2] if len(parts) > 2 else "-"
                status = parts[3] if len(parts) > 3 else "Pending"
                cursor.execute("INSERT INTO trades (trade_partner, cards_given, cards_received, status, timestamp) VALUES (?, ?, ?, ?, ?)", (partner, given, received, status, ts))
                conn.commit()
                reply = f"[{ts}] Catatan Trade ditambahkan: Partner '{partner}' [Give: {given} | Receive: {received}] -> Status: {status}"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'trade add [partner] | [cards given] | [cards received] | [status]'"
        elif cmd_l.startswith("want add "):
            content = cmd[9:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                cname = parts[0]
                tprice = parts[1] if len(parts) > 1 else "Rp 0"
                priority = parts[2] if len(parts) > 2 else "Med"
                cursor.execute("INSERT INTO wants (card_name, target_price, priority, timestamp) VALUES (?, ?, ?, ?)", (cname, tprice, priority, ts))
                conn.commit()
                reply = f"[{ts}] Wants List ditambahkan: '{cname}' [Target: {tprice}, Prioritas: {priority}]"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'want add [nama kartu] | [target harga] | [prioritas]'"
        elif cmd_l.startswith("inv add "):
            content = cmd[8:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                cname = parts[0]
                rarity = parts[1] if len(parts) > 1 else "Common"
                cond = parts[2] if len(parts) > 2 else "Near Mint"
                qty = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 1
                cursor.execute("INSERT INTO inventory (card_name, rarity, condition, qty, timestamp) VALUES (?, ?, ?, ?, ?)", (cname, rarity, cond, qty, ts))
                conn.commit()
                reply = f"[{ts}] Inventaris Kartu ditambahkan: '{cname}' [{rarity}, {cond}] x{qty}"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'inv add [nama kartu] | [rarity] | [kondisi] | [jumlah]'"
        elif cmd_l.startswith("draw "):
            dname = cmd[5:].strip()
            cursor.execute("SELECT main_cards FROM decks WHERE LOWER(name) = ?", (dname.lower(),))
            row = cursor.fetchone()
            if row and row[0]:
                card_text = row[0]
                card_pool = [c.strip() for c in card_text.split(",") if c.strip()]
                if len(card_pool) >= 5:
                    drawn = random.sample(card_pool, 5)
                else:
                    drawn = card_pool * 3
                    random.shuffle(drawn)
                    drawn = drawn[:5]
                hand_str = ", ".join(drawn)
                cursor.execute("INSERT INTO simulations (deck_name, hand_cards, timestamp) VALUES (?, ?, ?)", (dname, hand_str, ts))
                conn.commit()
                reply = f"[{ts}] Hand Simulasi untuk '{dname}':\\n• [{hand_str}]"
            else:
                cursor.execute("SELECT name FROM cards")
                c_rows = [r[0] for r in cursor.fetchall()]
                if len(c_rows) >= 5:
                    drawn = random.sample(c_rows, 5)
                    hand_str = ", ".join(drawn)
                    cursor.execute("INSERT INTO simulations (deck_name, hand_cards, timestamp) VALUES (?, ?, ?)", (dname, hand_str, ts))
                    conn.commit()
                    reply = f"[{ts}] Deck tidak ditemukan di Vault, mengambil dari Basis Data Kartu:\\n• [{hand_str}]"
                else:
                    reply = f"[{ts}] Deck '{dname}' tidak ditemukan di Vault dan basis data kartu kurang dari 5."
        elif cmd_l.startswith("deck"):
            content = cmd[4:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                dname = parts[0]
                strat = parts[1] if len(parts) > 1 else "Custom Strategy"
                mcards = parts[2] if len(parts) > 2 else "-"
                cursor.execute("INSERT INTO decks (name, strategy, main_cards, timestamp) VALUES (?, ?, ?, ?)", (dname, strat, mcards, ts))
                conn.commit()
                reply = f"[{ts}] Deck '{dname}' berhasil disimpan ke Deck Vault!"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'deck [nama deck] | [strategi] | [kartu utama]'"
        elif cmd_l.startswith("sideboard"):
            content = cmd[9:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                arch = parts[0]
                cin = parts[1] if len(parts) > 1 else "-"
                cout = parts[2] if len(parts) > 2 else "-"
                notes = parts[3] if len(parts) > 3 else "-"
                cursor.execute("INSERT INTO sideboards (archetype, cards_in, cards_out, notes, timestamp) VALUES (?, ?, ?, ?, ?)", (arch, cin, cout, notes, ts))
                conn.commit()
                reply = f"[{ts}] Sideboard Matrix untuk '{arch}' berhasil disimpan!"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'sideboard [archetype] | [cards in] | [cards out] | [catatan]'"
        elif cmd_l.startswith("log match"):
            content = cmd[9:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                matchup_part = parts[0]
                result_part = parts[1] if len(parts) > 1 else "WIN"
                notes_part = parts[2] if len(parts) > 2 else "-"
                if " vs " in matchup_part:
                    deck_name, opponent = [x.strip() for x in matchup_part.split(" vs ", 1)]
                else:
                    return jsonify({"reply": f"[{ts}] Format salah. Gunakan: 'log match [deck] vs [opponent] | [WIN/LOSS] | [catatan]'"})
                
                cursor.execute("INSERT INTO matches (deck_name, opponent, result, notes, timestamp) VALUES (?, ?, ?, ?, ?)", (deck_name, opponent, result_part, notes_part, ts))
                conn.commit()
                reply = f"[{ts}] Match Dicatat! [{deck_name} vs {opponent}] -> Result: {result_part.upper()}"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'log match [deck] vs [opponent] | [WIN/LOSS] | [catatan]'"
        elif cmd_l.startswith("add card"):
            content = cmd[8:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                cname = parts[0]
                cat = parts[1] if len(parts) > 1 else "General"
                eff = parts[2] if len(parts) > 2 else "-"
                cursor.execute("INSERT INTO cards (name, category, effect, timestamp) VALUES (?, ?, ?, ?)", (cname, cat, eff, ts))
                conn.commit()
                reply = f"[{ts}] Kartu '{cname}' [{cat}] berhasil disimpan ke basis data!"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'add card [nama] | [kategori] | [efek]'"
        elif cmd_l.startswith("prob"):
            content = cmd[4:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                if len(parts) >= 4:
                    N = int(parts[0])
                    K = int(parts[1])
                    n = int(parts[2])
                    target_min = int(parts[3])
                    prob_sum = 0.0
                    for k_i in range(target_min, min(K, n) + 1):
                        prob_sum += hypergeometric(k_i, N, K, n)
                    pct = prob_sum * 100
                    reply = f"[{ts}] Kalkulasi Peluang Hipergeometrik:\\n• Ukuran Deck (N): {N}\\n• Kopi di Deck (K): {K}\\n• Kartu Ditarik (n): {n}\\n• Target Minimal (>= {target_min}): {pct:.2f}%"
                else:
                    reply = f"[{ts}] Format kurang lengkap. Gunakan: 'prob [deck_size] | [copies] | [hand_size] | [target_min]'"
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'prob [deck_size] | [copies] | [hand_size] | [target_min]'"
        elif cmd_l.startswith("score match"):
            content = cmd[11:].strip()
            if "|" in content:
                parts = [p.strip() for p in content.split("|")]
                matchup = parts[0]
                winner = parts[1] if len(parts) > 1 else ""
                if " vs " in matchup:
                    p1, p2 = [x.strip() for x in matchup.split(" vs ", 1)]
                else:
                    return jsonify({"reply": f"[{ts}] Format salah. Gunakan: 'score match [p1] vs [p2] | [pemenang]'"})
                
                loser = p2 if winner.lower() == p1.lower() else p1
                
                cursor.execute("SELECT id, points, wins FROM players WHERE LOWER(name) = ?", (winner.lower(),))
                w_row = cursor.fetchone()
                if w_row:
                    cursor.execute("UPDATE players SET points = points + 3, wins = wins + 1 WHERE id = ?", (w_row[0],))
                else:
                    cursor.execute("INSERT INTO players (name, points, wins, losses, timestamp) VALUES (?, 3, 1, 0, ?)", (winner, ts))
                
                cursor.execute("SELECT id, losses FROM players WHERE LOWER(name) = ?", (loser.lower(),))
                l_row = cursor.fetchone()
                if l_row:
                    cursor.execute("UPDATE players SET losses = losses + 1 WHERE id = ?", (l_row[0],))
                else:
                    cursor.execute("INSERT INTO players (name, points, wins, losses, timestamp) VALUES (?, 0, 0, 1, ?)", (loser, ts))
                
                conn.commit()
                reply = f"[{ts}] Skor Match Dicatat! Pemenang: {winner} (+3 PTS), Kalah: {loser} (+1 L)."
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'score match [p1] vs [p2] | [pemenang]'"
        elif cmd_l.startswith("register"):
            pname = cmd[8:].strip()
            if pname:
                cursor.execute("INSERT INTO players (name, points, wins, losses, timestamp) VALUES (?, 0, 0, 0, ?)", (pname, ts))
                conn.commit()
                reply = f"[{ts}] Player '{pname}' berhasil didaftarkan."
            else:
                reply = f"[{ts}] Format salah. Gunakan: 'register [nama player]'"
        elif cmd_l == "standings":
            cursor.execute("SELECT name, points, wins, losses FROM players ORDER BY points DESC")
            rows = cursor.fetchall()
            reply = f"[{ts}] Klasemen Swiss:\\n" + "\\n".join([f"- {r[0]}: {r[1]} PTS ({r[2]}W/{r[3]}L)" for r in rows]) if rows else f"[{ts}] Belum ada player."
        elif cmd_l == "pairings":
            cursor.execute("SELECT name FROM players")
            rows = [r[0] for r in cursor.fetchall()]
            if len(rows) >= 2:
                random.shuffle(rows)
                pairs = [f"{rows[i]} vs {rows[i+1]}" for i in range(0, len(rows)-1, 2)]
                reply = f"[{ts}] Pairings:\\n" + "\\n".join([f"• {p}" for p in pairs])
            else:
                reply = f"[{ts}] Minimal butuh 2 player."
        else:
            reply = f"[{ts}] Perintah '{cmd}' diproses di bawah Protokol Al-Haqq (ICAM / Syams Maulana)."
    except Exception as e:
        reply = f"[{ts}] Error: {str(e)}"
    finally:
        conn.close()
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
