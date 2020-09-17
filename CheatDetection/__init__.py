# * This file is set to test pose classification using YMCA example on a webcam
# Preceded by YMCATest.py and YMCATest.ipynb
from .utils import (
    NormalizePoseCollection,
    NormalizePose,
    ReshapePoseCollection,
    ReshapePose,
    RandomizePose,
    CreateArtificialPoseCollection,
    ConvertToDataFrame,
    GetColumnNames,
)
import sys
import cv2
import os
from sys import platform
import argparse
import math
import numpy as np
import random
import copy
import pandas as pd
import glob
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import concurrent.futures


# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + './python/openpose/Release')
        # os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        os.add_dll_directory(dir_path + './x64/Release')
        os.add_dll_directory(dir_path + './bin')
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('./python')
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

class CheatDetection:
    def __init__(self):
        params = dict()
        params["model_folder"] =dir_path + "./models/"
        params["net_resolution"] = "-1x80"
        params["output_resolution"] = "-1x320"

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()
        self.datum = op.Datum()

        # Starting XGBoost
        self.model = XGBClassifier()
        self.model.load_model(dir_path+"./XGB_YMCA.model")

        # Process Encoder
        self.le = LabelEncoder()
        self.le.fit(["Y", "M", "C", "A"])

    def GeneratePose(self, img):
        self.datum.cvInputData = img
        self.opWrapper.emplaceAndPop([self.datum])
        return self.datum.cvOutputData

    def DetectCheat(self):
        poseCollection = self.datum.poseKeypoints
        detectedPoses = []
        if poseCollection.ndim != 0:
            newPoseCollection = NormalizePoseCollection(poseCollection)
            newPoseCollection = ReshapePoseCollection(newPoseCollection)
            newPoseCollection = ConvertToDataFrame(newPoseCollection)
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                newPoseCollection = [ row for index,row in newPoseCollection.iterrows() ]
                pred = executor.map(self.model.predict, newPoseCollection)
                pred = map(self.le.inverse_transform, pred)
                detectedPoses.extend(list(pred))
        
        self.datum.cvOutputData = cv2.putText(
            self.datum.cvOutputData,
            ' '.join(map(str, detectedPoses)),
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

        return self.datum.cvOutputData



# # Process Webcam
# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#     datum.cvInputData = frame
#     # * Process Image
#     opWrapper.emplaceAndPop([datum])
#     poseCollection = datum.poseKeypoints
#     detectedPoses = []
#     if poseCollection.ndim != 0:
#         for pose in poseCollection:
#             # * Normalize Pose Collection
#             pose = NormalizePose(pose)
#             #  * Reshaping of Pose Collection
#             pose = ReshapePose(pose)
#             # * Creating a Pose Collection DataFrame
#             pose = ConvertToDataFrame(pose)
#             # * Classify Pose
#             pred = model.predict(pose)
#             pred = le.inverse_transform(pred)
#             detectedPoses.append(pred)
#     print(detectedPoses)
#     cv2.imshow(
#         "Frame",
#         cv2.putText(
#             datum.cvOutputData,
#             f"{detectedPoses}",
#             (10, 450),
#             font,
#             3,
#             (0, 255, 0),
#             2,
#             cv2.LINE_AA,
#         ),
#     )
#     # cv2.imshow("Frame", datum.cvOutputData)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()
