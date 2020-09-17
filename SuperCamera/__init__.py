from .camera_opencv import Camera
from .base_camera import BaseCamera
from .base_camera import CameraEvent
from CheatDetection import CheatDetection
import cv2
import time
import os
from imutils.video import FPS
import threading


class SuperCamera(Camera):
    """ [UNUSED] Monolithic approach of having a Class inherit all Functionality from threading,
        to generator throttling to Image Processing to Pose Estimation, then finally to Cheat Detection    

    Args:
        Camera (Camera_OpenCV): Sets Grandparent to use camera as video source

    Raises:
        RuntimeError: Checks Camera Functionality

    Yields:
        Jpeg: Produces encoded from camera, and processed with Cheat Detection
    """
    cheatDetection = CheatDetection()
    threadCount = threading.active_count()

    def __init__(self):
        super(SuperCamera, self).__init__()

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        # camera = cv2.VideoCapture(os.path.dirname(os.path.realpath(__file__))+"/sample.mp4")
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        while True:
            # read current frame
            _, img = camera.read()
            #OpenPose API Generated Estimations
            img = SuperCamera.cheatDetection.GeneratePose(img)
            # XGBoost Cheat Detection Prediction
            img = SuperCamera.cheatDetection.DetectCheat()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()


    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        SuperCamera.fps= FPS().start()
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None

    # * This EXPERIMENT USES MULTITHREADED QEUE TO OPTIMIZE OPENCV READ.
    # ! Does not work because reading is segmented into a thread that forces reading of all frames at lesser priority
    # ! TL;DR Too slow for webcam needs potential fixing and maybe become useful
    # fvs = None
    # fps = None
    # @staticmethod
    # def frames():
    #     # camera = cv2.VideoCapture(Camera.video_source)
    #     if not SuperCamera.fvs:
    #         SuperCamera.fvs= FileVideoStream(os.path.dirname(os.path.realpath(__file__))+"/sample.mp4").start()
    #     while SuperCamera.fvs.more():
    #         # read current frame
    #         img = SuperCamera.fvs.read()
    #         #OpenPose API Generated Estimations
    #         # img = SuperCamera.cheatDetection.GeneratePose(img)
    #         # XGBoost Cheat Detection Prediction
    #         # img = SuperCamera.cheatDetection.DetectCheat()

    #         SuperCamera.fps.update()
    #         # encode as a jpeg image and return it
    #         yield cv2.imencode('.jpg', img)[1].tobytes()