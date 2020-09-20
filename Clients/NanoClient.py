# from NanoClient.CVClient import CVClient
from Clients.Streamer import Streamer, sio
import cv2
import base64
import time
import threading

lock = threading.Lock()

class NanoClient:
    streamer = None
    camera = 0
    enabled = False
    isRunning = False
    Cap = None

    def __init__(self, _camera, _server_addr, _stream_fps, _server_port):
        NanoClient.streamer = Streamer('nano', _server_addr,
                        _server_port, _stream_fps).setup()
        sio.wait()
        NanoClient.camera = _camera

    @staticmethod
    @sio.event
    def disconnect():
        print('[INFO] Disconnected from server.')
        # NanoClient.enabled = False

    @staticmethod
    @sio.on('enable_camera', namespace='/nano')
    def enable_camera(message):
        if NanoClient.enabled or NanoClient.isRunning:
            print(f'[INFO] Camera already enabled')
            NanoClient.Cap.release()
            return
        print("[INFO] Enabled Camera on Nano")
        NanoClient.enabled = True
        CVThread = threading.Thread(target=CVCamera)
        CVThread.setDaemon(True)
        CVThread.start()

    @staticmethod
    @sio.on('disable_camera', namespace='/nano')
    def disable_camera(self):
        if not NanoClient.enabled:
            print(f'[INFO] Camera already disabled')
            return
        print("[INFO] Disable Camera on Nano")
        NanoClient.enabled = False

def CVCamera():
    NanoClient.isRunning = True
    NanoClient.Cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not NanoClient.Cap.isOpened():
        raise RuntimeError('Could not start camera.')
    while NanoClient.enabled:
        time.sleep(0.01)
        with lock:
            _, img = NanoClient.Cap.read()
            NanoClient.streamer.send_data(img,1)
        # print("sent image to server")
    NanoClient.Cap.release()
    NanoClient.isRunning = False

