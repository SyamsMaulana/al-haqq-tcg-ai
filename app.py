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
