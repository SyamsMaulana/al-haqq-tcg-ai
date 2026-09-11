from flask import Flask, render_template, request, jsonify

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
