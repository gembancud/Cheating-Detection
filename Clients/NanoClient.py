# from NanoClient.CVClient import CVClient
from Clients.Streamer import Streamer, sio
import cv2
import base64
import time
import threading

streamer = None
camera = 0
enabled = False
isRunning = False
Cap = None


@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')
    global enabled
    enabled = False


def CVCamera():
    global isRunning
    isRunning = True
    global Cap
    Cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not Cap.isOpened():
        raise RuntimeError('Could not start camera.')
    while enabled:
        time.sleep(0.01)
        _, img = Cap.read()
        streamer.send_data(Streamer.convert_image_to_jpeg(img))
        # print("sent image to server")
    Cap.release()
    isRunning = False


CVThread = threading.Thread(target=CVCamera)


def nanoClient(_camera, _server_addr, _stream_fps, _server_port):
    global streamer
    streamer = Streamer('nano', _server_addr,
                        _server_port, _stream_fps).setup()
    sio.wait()

    global camera
    camera = _camera

    global CVThread
    CVThread = threading.Thread(target=CVCamera)
    CVThread.setDaemon(True)


@sio.on('enable_camera', namespace='/nano')
def enable_camera(message):
    global enabled
    if enabled or isRunning:
        print(f'[INFO] Camera already enabled')
        Cap.release()
        return
    print("[INFO] Enabled Camera on Nano")
    enabled = True
    global CVThread
    CVThread = threading.Thread(target=CVCamera)
    CVThread.setDaemon(True)
    CVThread.start()


@sio.on('disable_camera', namespace='/nano')
def disable_camera(self):
    global enabled
    if not enabled:
        print(f'[INFO] Camera already disabled')
        return
    print("[INFO] Disable Camera on Nano")
    enabled = False
    global CVThread
    CVThread = threading.Thread(target=CVCamera)
    CVThread.setDaemon(True)

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
