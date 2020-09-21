from flask import Flask, render_template, Response, request
from engineio.payload import Payload
from flask_socketio import SocketIO

Payload.max_decode_packets = 100
app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

@app.route('/')
def index():
    return render_template('index.html')

# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(SuperCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect', namespace='/web')
def connect_web():
    print('[INFO] Web client connected: {}'.format(request.sid))
    socketio.emit('enable_camera', {}, namespace='/nano')
    socketio.emit('enable_detection', {}, namespace='/cd')


@socketio.on('disconnect', namespace='/web')
def disconnect_web():
    print('[INFO] Web client disconnected: {}'.format(request.sid))
    socketio.emit('disable_camera', {}, namespace='/nano')
    socketio.emit('disable_detection', {}, namespace='/cd')


@socketio.on('connect', namespace='/nano')
def connect_nano():
    print('[INFO] nano client connected: {}'.format(request.sid))


@socketio.on('disconnect', namespace='/nano')
def disconnect_nano():
    print('[INFO] nano client disconnected: {}'.format(request.sid))


@socketio.on('connect', namespace='/cd')
def connect_nano():
    print('[INFO] Cheat Detection client connected: {}'.format(request.sid))


@socketio.on('disconnect', namespace='/cd')
def disconnect_nano():
    print('[INFO] Cheat Detection disconnected: {}'.format(request.sid))


@socketio.on('nano2server')
def handle_nano_message(message):
    print("pushing to cheat detection")
    # socketio.emit('push_to_imageQueue', message, namespace='/cd')
    socketio.emit('change_web_image', message, namespace='/web')


# @socketio.on('cd2server')
# def handle_cheat_detection(message):
#     print("updating image")
#     socketio.emit('change_web_image', message, namespace='/web')


