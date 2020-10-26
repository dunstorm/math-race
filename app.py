from flask import Flask, render_template, request
from flask_socketio import SocketIO
import random
import json

app = Flask(__name__)
app.debug = False
# app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

# socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins="*")

players = []


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace="/race")
def on_connect():
    print("Connected: %s" % request.sid)


@socketio.on('joined', namespace="/race")
def handle_joined(data):
    global players
    players.append({
        "sid": request.sid,
        "name": data["name"],
        "points": 0
    })
    socketio.emit('updateBoard', players, namespace="/race")


@socketio.on('increaseRank', namespace="/race")
def handle_increase_rank():
    global players

    players = list(map(lambda x: {"sid": x['sid'], "points": x['points']+1,
                                  "name": x['name']} if x['sid'] == request.sid else x, players))
    players = sorted(players, key=lambda k: k['points'], reverse=True)
    socketio.emit('updateBoard', players, namespace="/race")


@socketio.on('question', namespace="/race")
def handle_question():
    actions = ["addition", "subtraction"]

    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    action = random.choice(actions)
    answer = None

    if action == 'addition':
        answer = num1 + num2
    elif action == 'subtraction':
        answer = num1 - num2
    elif action == 'multiplication':
        answer = num1 * num2

    data = {
        "num1": num1,
        "num2": num2,
        "action": action,
        "answer": answer
    }

    socketio.emit('newQuestion', data, namespace="/race")


@socketio.on('disconnect', namespace="/race")
def on_disconnect():
    global players
    players = list(filter(lambda x: x["sid"] != request.sid, players))
    print("Disconnected: %s" % request.sid)
    socketio.emit('updateBoard', players, namespace="/race")


if __name__ == '__main__':
    socketio.run(app)
