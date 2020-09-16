# from NanoClient.CVClient import CVClient
from Clients.Streamer import Streamer, sio
import cv2
import base64
import time
import threading

streamer = None
camera = 0
enabled = False

def CVCamera():
    global camera,enabled
    Cap = cv2.VideoCapture(camera)
    if not Cap.isOpened():
        raise RuntimeError('Could not start camera.')
    while enabled:
        _, img = Cap.read()
        streamer.send_data(_convert_image_to_jpeg(img))
    Cap.release()
CVThread = threading.Thread(target=CVCamera)
CVThread.setDaemon(True)

def nanoClient(_camera, _server_addr, _stream_fps, _server_port):
    print('passed here')
    global streamer 
    streamer =  Streamer('nano', _server_addr, _server_port, _stream_fps).setup()
    sio.wait()

    global camera
    camera = _camera


@sio.on('enable_camera', namespace='/nano')
def enable_camera(message):
    print("[INFO] Enabled Camera on Nano")
    global enabled,CVThread
    if enabled:
        print(f'[INFO] Camera already enabled')
        return
    enabled =True
    CVThread.start()


@sio.on('disable_camera', namespace='/nano')
def disable_camera(self):
    print("[INFO] Disable Camera on Nano")
    global enabled
    if not enabled:
        print(f'[INFO] Camera already disabled')
        return
    enabled= False

    # try:
        # streamer = Streamer('nano', server_addr, server_port, stream_fps).setup()
        # if not camera.isOpened():
        #     raise RuntimeError('Could not start camera.')
        # while True:
        #     streamer.sio.wait()
        #     _, img = camera.read()
        #     streamer.send_data(_convert_image_to_jpeg(img))
        #     # cv2.imshow("NanoClient", img)
        #     # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     #     break
        #     # if streamer.check_exit():
        #     #     break
    # finally:
    #     if streamer is not None:
    #         streamer.close()
    #     print("Program Ending")

def _convert_image_to_jpeg(image):
    # Encode frame as jpeg
    frame = cv2.imencode('.jpg', image)[1].tobytes()
    # Encode frame in base64 representation and remove
    # utf-8 encoding
    frame = base64.b64encode(frame).decode('utf-8')
    return "data:image/jpeg;base64,{}".format(frame)


# class NanoClient:
#     streamer = None
#     camera = None
#     fps = 0
#     enabled = False
#     thread = None
#     stop = False

#     def __init__(self, addr, port, fps, camera):
#         NanoClient.streamer = Streamer('nano', addr, port, fps).setup()
#         NanoClient.camera = camera
#         NanoClient.fps = fps
#         NanoClient.enabled = False
#         NanoClient.thread = None
#         NanoClient.stop = False
#         NanoClient.streamer.sio.wait()
        
#     def enable_camera(self):
#         print("Enabled Camera on Nano")
#         if NanoClient.enabled:
#             print(f'[INFO] Camera already enabled')
#             return
#         NanoClient.enabled = True
#         NanoClient.thread = threading.Thread(target=NanoClient.CVCamera)
#         NanoClient.thread.start()
    
#     def disable_camera(self):
#         if not self.enabled:
#             return
#         print(f'[INFO] Camera already disable')
#         self.enabled = False

#     def CVCamera(self):
#         camera = cv2.VideoCapture(self.camera)
#         if not camera.isOpened():
#             raise RuntimeError('Could not start camera.')

#         while True:
#             if not self.enabled:
#                 break
#             _, img = camera.read()
#             streamer.send_data(_convert_image_to_jpeg(img))
#         camera.release()

#     @staticmethod
#     def _convert_image_to_jpeg(image):
#         # Encode frame as jpeg
#         frame = cv2.imencode('.jpg', image)[1].tobytes()
#         # Encode frame in base64 representation and remove
#         # utf-8 encoding
#         frame = base64.b64encode(frame).decode('utf-8')
#         return "data:image/jpeg;base64,{}".format(frame)

