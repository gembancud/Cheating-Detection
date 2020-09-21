from Clients.Streamer import Streamer, sio
from CheatDetection import CheatDetection
import cv2
import base64
import time
import threading
from collections import deque
import copy
import gc

lock = threading.Lock()

class CDClient:
    streamer = None
    enabled = False

    imageQueue = deque([])
    # cheatDetection = CheatDetection()

    def __init__(self,_server_addr, _stream_fps, _server_port):
        CDClient.streamer = Streamer('cd', _server_addr, _server_port, _stream_fps).setup()
        sio.wait()

    @staticmethod
    @sio.event
    def disconnect():
        print('[INFO] Disconnected from server.')
        # CDClient.enabled = False

    @staticmethod
    @sio.on('enable_detection', namespace='/cd')
    def enable_detection(message):
        print("[INFO] Enabled Cheating Detection")
        if CDClient.enabled:
            print(f'[INFO] Cheating Detection already enabled')
            return
        CDClient.enabled = True
        ProcessFramesThread = threading.Thread(target=ProcessFrames)
        # ProcessFramesThread.setDaemon(True)
        ProcessFramesThread.start()

    @staticmethod
    @sio.on('disable_detection', namespace='/cd')
    def disable_detection(message):
        print("[INFO] Disabling Cheating Detection")
        if not CDClient.enabled:
            print(f'[INFO] Cheating Detection already disabled')
            return
        CDClient.enabled = False

    @staticmethod
    @sio.on('push_to_imageQueue', namespace='/cd')
    def push_to_imageQueue(message):
        with lock:
            image = Streamer.convert_jpeg_to_image(message['message'])
            CDClient.imageQueue.append(image)
            print("Image Received")

def ProcessFrames():
    while CDClient.enabled:
        time.sleep(0.01)
        with lock:
            if not CDClient.imageQueue:
                time.sleep(0.1)
                continue
            frame = CDClient.imageQueue.pop()
            CDClient.imageQueue.clear()
            # frame = CDClient.cheatDetection.GeneratePose(frame)
            # frame = CDClient.cheatDetection.DetectCheat()
            CDClient.streamer.send_data(frame,1)
            # print("Done Processing Cheat Detection")
        # print(f"collected{gc.collect()}")
    print("[INFO] ProcessFrames Thread is stopped")
