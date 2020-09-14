from flask import Flask, render_template, Response, request
# from SuperCamera import SuperCamera
from flask_socketio import SocketIO
# from SuperCamera.camera_opencv import Camera
from engineio.payload import Payload

Payload.max_decode_packets = 50
app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(SuperCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect', namespace='/web')
def connect_web():
   print('[INFO] Web client connected: {}'.format(request.sid))

@socketio.on('disconnect', namespace='/web')
def disconnect_web():
    print('[INFO] Web client disconnected: {}'.format(request.sid))

@socketio.on('connect', namespace='/cv')
def connect_cv():
   print('[INFO] CV client connected: {}'.format(request.sid))
   socketio.emit('oten', 'oten2')

@socketio.on('disconnect', namespace='/cv')
def disconnect_cv():
   print('[INFO] CV client disconnected: {}'.format(request.sid))

@socketio.on('cv2server')
def handle_cv_message(message):
    socketio.emit('server2web', message, namespace='/web')