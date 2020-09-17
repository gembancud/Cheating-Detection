from Clients.Streamer import Streamer, sio
from CheatDetection import CheatDetection
import cv2
import base64
import time
import threading
from collections import deque

streamer = None
enabled = False
cheatDetection = CheatDetection()
image = None
imageChanged = False
# imageQueue = deque([])
# outputQueue = deque([])
enabled = False

@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')
    global enabled
    enabled = False

def ProcessFrames():
    global imageChanged
    while enabled:
        # if not imageQueue:
        if image is None or not imageChanged:
            # print("image queue is empty!")
            time.sleep(0.5)
            continue
        # frame = imageQueue.popleft()
        frame = image
        output = cheatDetection.GeneratePose(frame)
        output = cheatDetection.DetectCheat()
        streamer.send_data(Streamer.convert_image_to_jpeg(output))
        imageChanged= True
ProcessFramesThread = threading.Thread(target=ProcessFrames)

# def OutputFrames():
#     while enabled:
#         if not outputQueue:
#             print("output queue is empty!")
#             time.sleep(0)
#             continue
#         output = outputQueue.popleft()
#         streamer.send_data(Streamer.convert_image_to_jpeg(output))
# OutputFramesThread = threading.Thread(target=OutputFrames)


def cheatDetectionClient(_server_addr, _stream_fps, _server_port):
    global streamer
    streamer =  Streamer('cd', _server_addr, _server_port, _stream_fps).setup()
    sio.wait()

    global ProcessFramesThread
    ProcessFramesThread= threading.Thread(target=ProcessFrames)
    ProcessFramesThread.setDaemon(True)
    # global OutputFramesThread
    # OutputFramesThread= threading.Thread(target=OutputFrames)
    # OutputFramesThread.setDaemon(True)



@sio.on('push_to_imageQueue', namespace='/cd')
def push_to_imageQueue(message):
    global image
    image = Streamer.convert_jpeg_to_image(message['message'])
    global imageChanged
    imageChanged = True
    # imageQueue = append(image)

@sio.on('enable_detection', namespace='/cd')
def enable_detection(message):
    print("[INFO] Enabled Cheating Detection")
    global enabled
    if enabled:
        print(f'[INFO] Cheating Detection already enabled')
        return
    enabled =True
    ProcessFramesThread.start()
    # OutputFramesThread.start()


@sio.on('disable_detection', namespace='/cd')
def disable_detection(self):
    print("[INFO] Disabled Cheating Detection")
    global enabled
    if not enabled:
        print(f'[INFO] Cheating Detection already disabled')
        return
    enabled= False
    global ProcessFramesThread
    ProcessFramesThread= threading.Thread(target=ProcessFrames)
    ProcessFramesThread.setDaemon(True)
    # global OutputFramesThread
    # OutputFramesThread= threading.Thread(target=OutputFrames)
    # OutputFramesThread.setDaemon(True)


