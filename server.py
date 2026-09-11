import os
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f"Pemain bergabung ke arena: {room}"}, room=room)

@socketio.on('player_action')
def handle_action(data):
    room = data['room']
    emit('game_update', data, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
