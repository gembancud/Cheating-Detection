import time
import socketio
import cv2
import base64
import threading
import numpy as np

sio = socketio.Client()

@sio.event
def connect():
    print('[INFO] Successfully connected to server.')

@sio.event
def connect_error(error):
    print('[INFO] Failed to connect to server.')

@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')

class Streamer:
    def __init__(self,namespace, server_addr='localhost', server_port=8000,stream_fps=60):
        self.namespace = namespace
        self.server_addr = server_addr
        self.server_port = server_port
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = (1/self._stream_fps)
        self.sio = sio

    def setup(self):
        print(f'[INFO] Connecting to server http://{self.server_addr}:{self.server_port}...')
        sio.connect(
                f'http://{self.server_addr}:{self.server_port}',
                transports=['websocket'],
                namespaces=[f'/{self.namespace}'])
        time.sleep(1)
        return self

    def send_data(self, message):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            sio.emit(
                    f'{self.namespace}2server',
                    {
                        'message': message,
                    })

    @staticmethod
    @sio.on('server2streamer')
    def receive_data(message):
        print('Received from receive_data()')

    def check_exit(self):
        pass

    def close(self):
        sio.disconnect()

    @staticmethod
    def convert_image_to_jpeg(image):
    # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        output = "data:image/jpeg;base64,{}".format(frame)
        return output

    @staticmethod
    def convert_jpeg_to_image(jpeg):
    # Encode frame as jpeg
        frame = jpeg.replace("data:image/jpeg;base64,","").encode('utf-8')
        im_bytes = base64.b64decode(frame)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)         # utf-8 encoding
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        return img

