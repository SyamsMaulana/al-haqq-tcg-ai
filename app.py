from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.get_json()
    cmd = data.get('command', '')
    reply = f"Perintah diterima: '{cmd}'. Ekosistem Gold MauL dan protokol Al-Haqq aktif."
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
