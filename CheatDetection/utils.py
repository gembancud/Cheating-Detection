import math
import numpy as np
import random
import copy
import pandas as pd
import cv2

# THIS FUNCTION CONVERTS THE INPUTTED POSE COLLECTION INTO A DISTRIBUTION [0,1] FOR EVERY KEYPOINT.
# IT ADDITIONALLY FLIPS THE Y DIMENSION TO REFLECT A CARTESIAN COORDINATE SYSTEM
# THE CONVERTED OUTPUT IS IN THE FORMAT OF NP ARRAY


def NormalizePoseCollection(poseCollection, flipY=True):
    convertedPoseCollection = []
    for pose in poseCollection:
        # convertedPose = []
        # # Compute the Maximum bounds in dimensions X and Y of the pose
        # maxX, minX = -math.inf, math.inf
        # maxY, minY = -math.inf, math.inf
        # for keyPoint in pose:
        #     if keyPoint[2] == 0:
        #         continue
        #     if keyPoint[0] > maxX:
        #         maxX = keyPoint[0]
        #     if keyPoint[0] < minX:
        #         minX = keyPoint[0]
        #     if keyPoint[1] > maxY:
        #         maxY = keyPoint[1]
        #     if keyPoint[1] < minY:
        #         minY = keyPoint[1]
        # frameDiffX = maxX - minX
        # frameDiffY = maxY - minY

        # # Convert the Coordinates to normalized values
        # # NOTE: The Origin of the KeyPoints is located at the topleft of the image and is forcibly flipped around the X axis to
        # # reflect the rectangular coordinate system where its logical Origin is now at the bottomleft.
        # for keyPoint in pose:
        #     convertedKeyPoint = [0, 0, 0]
        #     if keyPoint[2] == 0:
        #         convertedPose.append(convertedKeyPoint)
        #         continue
        #     convertedKeyPoint[0] = (keyPoint[0] - minX) / (frameDiffX)
        #     if flipY == True:
        #         convertedKeyPoint[1] = (keyPoint[1] - minY) / (frameDiffY)
        #     else:
        #         convertedKeyPoint[1] = (maxY - keyPoint[1]) / (frameDiffY)
        #     convertedKeyPoint[2] = keyPoint[2]
        #     convertedPose.append(convertedKeyPoint)
        convertedPose = NormalizePose(pose, flipY=flipY)
        convertedPoseCollection.append(convertedPose)

    return np.array(convertedPoseCollection)


def NormalizePose(pose, flipY=True):
    convertedPose = []
    # Compute the Maximum bounds in dimensions X and Y of the pose
    maxX, minX = -math.inf, math.inf
    maxY, minY = -math.inf, math.inf
    for keyPoint in pose:
        if keyPoint[2] == 0:
            continue
        if keyPoint[0] > maxX:
            maxX = keyPoint[0]
        if keyPoint[0] < minX:
            minX = keyPoint[0]
        if keyPoint[1] > maxY:
            maxY = keyPoint[1]
        if keyPoint[1] < minY:
            minY = keyPoint[1]
    frameDiffX = maxX - minX
    frameDiffY = maxY - minY
    # Convert the Coordinates to normalized values
    # NOTE: The Origin of the KeyPoints is located at the topleft of the image and is forcibly flipped around the X axis to
    # reflect the rectangular coordinate system where its logical Origin is now at the bottomleft.
    for keyPoint in pose:
        convertedKeyPoint = [0, 0, 0]
        if keyPoint[2] == 0:
            convertedPose.append(convertedKeyPoint)
            continue
        convertedKeyPoint[0] = (keyPoint[0] - minX) / (frameDiffX)
        if flipY == True:
            convertedKeyPoint[1] = (keyPoint[1] - minY) / (frameDiffY)
        else:
            convertedKeyPoint[1] = (maxY - keyPoint[1]) / (frameDiffY)
        convertedKeyPoint[2] = keyPoint[2]
        convertedPose.append(convertedKeyPoint)
    return convertedPose


# ACCEPTS AN NP ARRAY POSE COLLECTION AND RESHAPES
# from (numPoses, numKeyPoints,KeyPointVector) to (numPoses, numKeyPoints*KeyPointVector)


def ReshapePoseCollection(poseCollection):
    numPoses, numKeyPoints, KeyPointVector = (
        poseCollection.shape[0],
        poseCollection.shape[1],
        poseCollection.shape[2],
    )
    poseCollection = np.reshape(
        poseCollection, (numPoses, numKeyPoints * KeyPointVector)
    )
    return poseCollection


# ACCEPTS AN NP ARRAY POSE  AND RESHAPES
# from (numKeyPoints,KeyPointVector) to (1, numKeyPoints*KeyPointVector)


def ReshapePose(pose):
    pose = np.array(pose)
    numKeyPoints, KeyPointVector = (
        pose.shape[0],
        pose.shape[1],
    )
    return [pose.flatten()]


# ACCEPTS AN NP ARRAY POSE AND RANDOMIZES ALL VALID KEYPOINTS ON A PERCENTAGE RANGE (Default 5%)


def RandomizePose(pose, range=0.05):
    newPose = copy.deepcopy(pose)
    for keyPoint in newPose:
        if keyPoint[2] == 0:
            continue
        keyPoint[0] *= 1 + random.uniform(-range, range)
        keyPoint[1] *= 1 + random.uniform(-range, range)
        keyPoint[2] *= 1 + random.uniform(-range, range)
    return newPose


# ACCEPTS AN NP ARRAY POSE COLLECTION AND GENERATES ARBITRARY NUMBER OF NEW POSES.
# RETURNS THE COLLECTION OF POSES GENERATED (NUMBER OF POSES x NUMBER OF CHILDREN PER POSE).


def CreateArtificialPoseCollection(poseCollection, numChildren=4):
    artificialPoseCollection = []
    for pose in poseCollection:
        for i in range(numChildren):
            newPose = RandomizePose(pose)
            artificialPoseCollection.append(newPose)
    return np.array(artificialPoseCollection)


# ACCEPTS AN NP ARRAY POSE COLLECTION AND CONVERTS INTO A DATAFRAME.
# IT MAY OPTIONALLY ADD A TARGET LABEL FOR ALL SAMPLES IN THE COLLECTION.
# IT THEN APPROPRIATELY RETURNS THAT DATAFRAME


def ConvertToDataFrame(poseCollection, label=None):
    columnNames = GetColumnNames()
    poseDF = pd.DataFrame(poseCollection, columns=columnNames)
    if label is not None:
        poseDF["label"] = label
    return poseDF


# GETS THE COLUMN NAMES FOR THE DATAFRAME OF THE POSE COLLECTION INTO A SINGLE LIST
def GetColumnNames(dim=None):
    # columnNames = []
    # for i in range(25):
    #     columnNames.append("kp" + str(i) + "_X")
    #     columnNames.append("kp" + str(i) + "_Y")
    #     columnNames.append("kp" + str(i) + "_Z")
    # return columnNames
    if dim == "x" or dim == "X":
        return
        ['kp0_X', 'kp1_X', 'kp2_X', 'kp3_X', 'kp4_X', 'kp5_X', 'kp6_X', 'kp7_X', 'kp8_X', 'kp9_X', 'kp10_X', 'kp11_X', 'kp12_X',
            'kp13_X', 'kp14_X', 'kp15_X', 'kp16_X', 'kp17_X', 'kp18_X', 'kp19_X', 'kp20_X', 'kp21_X', 'kp22_X', 'kp23_X', 'kp24_X']

    if dim == "y" or dim == "Y":
        return ['kp0_Y', 'kp1_Y', 'kp2_Y', 'kp3_Y', 'kp4_Y', 'kp5_Y', 'kp6_Y', 'kp7_Y', 'kp8_Y', 'kp9_Y', 'kp10_Y', 'kp11_Y',
                'kp12_Y', 'kp13_Y', 'kp14_Y', 'kp15_Y', 'kp16_Y', 'kp17_Y', 'kp18_Y', 'kp19_Y', 'kp20_Y', 'kp21_Y', 'kp22_Y', 'kp23_Y', 'kp24_Y']

    if dim == "z" or dim == "Z":
        return ['kp0_Z', 'kp1_Z', 'kp2_Z', 'kp3_Z', 'kp4_Z', 'kp5_Z', 'kp6_Z', 'kp7_Z', 'kp8_Z', 'kp9_Z', 'kp10_Z', 'kp11_Z', 'kp12_Z',
                'kp13_Z', 'kp14_Z', 'kp15_Z', 'kp16_Z', 'kp17_Z', 'kp18_Z', 'kp19_Z', 'kp20_Z', 'kp21_Z', 'kp22_Z', 'kp23_Z', 'kp24_Z']

    return ['kp0_X', 'kp0_Y', 'kp0_Z', 'kp1_X', 'kp1_Y', 'kp1_Z',
            'kp2_X', 'kp2_Y', 'kp2_Z', 'kp3_X', 'kp3_Y', 'kp3_Z', 'kp4_X',
            'kp4_Y', 'kp4_Z', 'kp5_X', 'kp5_Y', 'kp5_Z', 'kp6_X', 'kp6_Y',
            'kp6_Z', 'kp7_X', 'kp7_Y', 'kp7_Z', 'kp8_X', 'kp8_Y', 'kp8_Z',
            'kp9_X', 'kp9_Y', 'kp9_Z', 'kp10_X', 'kp10_Y', 'kp10_Z',
            'kp11_X', 'kp11_Y', 'kp11_Z', 'kp12_X', 'kp12_Y', 'kp12_Z',
            'kp13_X', 'kp13_Y', 'kp13_Z', 'kp14_X', 'kp14_Y', 'kp14_Z',
            'kp15_X', 'kp15_Y', 'kp15_Z', 'kp16_X', 'kp16_Y', 'kp16_Z',
            'kp17_X', 'kp17_Y', 'kp17_Z', 'kp18_X', 'kp18_Y', 'kp18_Z',
            'kp19_X', 'kp19_Y', 'kp19_Z', 'kp20_X', 'kp20_Y', 'kp20_Z',
            'kp21_X', 'kp21_Y', 'kp21_Z', 'kp22_X', 'kp22_Y', 'kp22_Z',
            'kp23_X', 'kp23_Y', 'kp23_Z', 'kp24_X', 'kp24_Y', 'kp24_Z']


def GetBoundingBoxCoords(pose):
    # Compute the Maximum bounds in dimensions X and Y of the pose
    maxX, minX = -math.inf, math.inf
    maxY, minY = -math.inf, math.inf
    for keyPoint in pose:
        if keyPoint[2] == 0:
            continue
        if keyPoint[0] > maxX:
            maxX = keyPoint[0]
        if keyPoint[0] < minX:
            minX = keyPoint[0]
        if keyPoint[1] > maxY:
            maxY = keyPoint[1]
        if keyPoint[1] < minY:
            minY = keyPoint[1]
    return [(minX, minY), (maxX, maxY)]


def DrawBoundingRectangle(image, point, color=(0, 0, 255), thickness=2):
    return cv2.rectangle(image, point[0], point[1], color, thickness)


X_COLUMNNAMES = ['kp0_X', 'kp1_X', 'kp2_X', 'kp3_X', 'kp4_X', 'kp5_X', 'kp6_X', 'kp7_X', 'kp8_X', 'kp9_X', 'kp10_X', 'kp11_X', 'kp12_X',
                 'kp13_X', 'kp14_X', 'kp15_X', 'kp16_X', 'kp17_X', 'kp18_X', 'kp19_X', 'kp20_X', 'kp21_X', 'kp22_X', 'kp23_X', 'kp24_X']
Y_COLUMNNAMES = ['kp0_Y', 'kp1_Y', 'kp2_Y', 'kp3_Y', 'kp4_Y', 'kp5_Y', 'kp6_Y', 'kp7_Y', 'kp8_Y', 'kp9_Y', 'kp10_Y', 'kp11_Y',
                 'kp12_Y', 'kp13_Y', 'kp14_Y', 'kp15_Y', 'kp16_Y', 'kp17_Y', 'kp18_Y', 'kp19_Y', 'kp20_Y', 'kp21_Y', 'kp22_Y', 'kp23_Y', 'kp24_Y']
Z_COLUMNNAMES = ['kp0_Z', 'kp1_Z', 'kp2_Z', 'kp3_Z', 'kp4_Z', 'kp5_Z', 'kp6_Z', 'kp7_Z', 'kp8_Z', 'kp9_Z', 'kp10_Z', 'kp11_Z', 'kp12_Z',
                 'kp13_Z', 'kp14_Z', 'kp15_Z', 'kp16_Z', 'kp17_Z', 'kp18_Z', 'kp19_Z', 'kp20_Z', 'kp21_Z', 'kp22_Z', 'kp23_Z', 'kp24_Z']
COLUMNNAMES = ['kp0_X', 'kp0_Y', 'kp0_Z', 'kp1_X', 'kp1_Y', 'kp1_Z',
               'kp2_X', 'kp2_Y', 'kp2_Z', 'kp3_X', 'kp3_Y', 'kp3_Z', 'kp4_X',
               'kp4_Y', 'kp4_Z', 'kp5_X', 'kp5_Y', 'kp5_Z', 'kp6_X', 'kp6_Y',
               'kp6_Z', 'kp7_X', 'kp7_Y', 'kp7_Z', 'kp8_X', 'kp8_Y', 'kp8_Z',
               'kp9_X', 'kp9_Y', 'kp9_Z', 'kp10_X', 'kp10_Y', 'kp10_Z',
               'kp11_X', 'kp11_Y', 'kp11_Z', 'kp12_X', 'kp12_Y', 'kp12_Z',
               'kp13_X', 'kp13_Y', 'kp13_Z', 'kp14_X', 'kp14_Y', 'kp14_Z',
               'kp15_X', 'kp15_Y', 'kp15_Z', 'kp16_X', 'kp16_Y', 'kp16_Z',
               'kp17_X', 'kp17_Y', 'kp17_Z', 'kp18_X', 'kp18_Y', 'kp18_Z',
               'kp19_X', 'kp19_Y', 'kp19_Z', 'kp20_X', 'kp20_Y', 'kp20_Z',
               'kp21_X', 'kp21_Y', 'kp21_Z', 'kp22_X', 'kp22_Y', 'kp22_Z',
               'kp23_X', 'kp23_Y', 'kp23_Z', 'kp24_X', 'kp24_Y', 'kp24_Z']

TAKE_FIRST = lambda s1, s2: s1
def NormalizeDataFrame(dataframe, flipY=True):
    # print(dataframe.head())
    # print(X_COLUMNNAMES)
    dfX = dataframe[X_COLUMNNAMES]
    dfY = dataframe[Y_COLUMNNAMES]

    print(dfX.head())
    print(dfY.head())

    maxX = dfX.loc[:, ~(dfX == 0.0)].max(axis=1)
    minX = dfX.loc[:, ~(dfX == 0.0)].min(axis=1)
    maxY = dfY.loc[:, ~(dfY == 0.0)].max(axis=1)
    minY = dfY.loc[:, ~(dfY == 0.0)].min(axis=1)

    frameDiffX = maxX - minX
    frameDiffY = maxY - minY

    dfX = dfX.subtract(minX)
    print(dfX.head())
    dfX = dfX.div(frameDiffX)
    print(dfX.head())

    dfY = dfY.subtract(minY)
    dfY = dfY.div(frameDiffY)


    print(dfX.head())
    print(dfY.head())
    rdf = pd.concat([dfX,dfY],axis=1)
    print(rdf.columns)
    print(f"rdf {rdf.shape} df {dataframe.shape}")

    return dataframe.combine(rdf,TAKE_FIRST)
