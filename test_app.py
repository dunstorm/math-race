import socketio

sio = socketio.Client()


@sio.on('newQuestion')
def on_question(data):
    print(data)


sio.connect('http://127.0.0.1:5000', namespaces=['/race'])
sio.emit('question', namespace='/race')
sio.disconnect()
