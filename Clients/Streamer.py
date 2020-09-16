import time
import socketio
import cv2
import base64
import threading

sio = socketio.Client()

@sio.event
def connect():
    print('[INFO] Successfully connected to server.')

@sio.event
def connect_error():
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

