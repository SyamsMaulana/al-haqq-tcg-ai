from flask import Flask, render_template, request, jsonify
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.get_json()
    cmd = data.get('command', '')
    reply = f"Perintah '{cmd}' diproses di bawah Protokol Al-Haqq (ICAM / Syams Maulana)."
    return jsonify({'reply': reply})

@app.route('/api/barcode', methods=['POST'])
def generate_barcode():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"living_barcode_{timestamp}.png"
    filepath = os.path.join(os.getcwd(), filename)
    
    payload = f"Al-Haqq Protocol | ICAM (Syams Maulana) | {timestamp}"
    img = qrcode.make(payload)
    img.save(filepath)
    
    return jsonify({'status': 'success', 'file': filename, 'message': 'Living Barcode berhasil dicetak.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

@app.route('/api/set-mode', methods=['POST'])
def set_mode():
    data = request.get_json()
    mode = data.get('mode', 'competitive')
    # Update active AI scoring weights based on mode selection
    return jsonify({"status": "success", "active_mode": mode})

from bounties import load_bounties, save_bounty

@app.route('/api/bounties', methods=['GET', 'POST'])
def handle_bounties():
    if request.method == 'POST':
        data = request.get_json()
        save_bounty(data.get('player'), data.get('title'), data.get('description'))
        return jsonify({"status": "success", "message": "Bounty logged!"})
    return jsonify(load_bounties())

from boss_raid import calculate_threats

@app.route('/api/boss-raid', methods=['POST'])
def boss_raid_calc():
    data = request.get_json()
    threats = calculate_threats(data.get('players', []))
    return jsonify(threats)
