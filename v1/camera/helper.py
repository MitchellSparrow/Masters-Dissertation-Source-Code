import cv2
import cv2.aruco as aruco
import numpy as np
from globals import *
import cvb


def configure_device(device: cvb.Device) -> None:
    dnode = device.node_maps['Device']
    dnode['Cust::autoBrightnessMode'].value = 'Active'  # Can be Off
    dnode['Std::BalanceWhiteAuto'].value = 'OnDemand'
    dnode['Std::AcquisitionFrameRate'].value = FPS
    #dnode['Std::Width'].value = CAMERA_WIDTH
    #dnode['Std::Height'].value = CAMERA_HEIGHT
    # dnode['Std::OffsetX'].value = CAMERA_HORIZONTAL_OFFSET
    # dnode['Std::OffsetY'].value = CAMERA_VERTICAL_OFFSET
    dnode['Std::TriggerMode'].value = 'Off'
    # dnode['Std::GevSCPSPacketSize'].value = 8192


def findArucoMarkers(img, markerSize=MARKER_SIZE, totalMarkers=50, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(
        gray, arucoDict, parameters=arucoParam)

    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]


def find_points(arucofound, img):
    tl = (0, 0)
    tr = (0, 0)
    br = (0, 0)
    bl = (0, 0)

    if len(arucofound[0]) == 4:
        for bbox, id in zip(arucofound[0], arucofound[1]):
            if id == 0:
                tl = bbox[0][0][0], bbox[0][0][1]
            elif id == 1:
                tr = bbox[0][1][0], bbox[0][1][1]
            elif id == 2:
                bl = bbox[0][3][0], bbox[0][3][1]
            elif id == 3:
                br = bbox[0][2][0], bbox[0][2][1]

    return np.array([tl, tr, br, bl])


def transform_image(img, points):
    #h, w, c = imgAug.shape
    #pts1 = np.array([tl, tr, br, bl])

    rotatedRect = cv2.minAreaRect(points)
    # Get rotated rect dimensions
    (x, y), (width, height), angle = rotatedRect
    # Get the 4 corners of the rotated rect
    # Top-left, top-right, bottom-right, bottom-left
    dstPts = [[0, 0], [width, 0], [width, height], [0, height]]
    # Get the transform
    matrix = cv2.getPerspectiveTransform(
        np.float32(points), np.float32(dstPts))
    # Transform the image
    out = cv2.warpPerspective(img, matrix, (int(width), int(height)))

    return out


def arucoAug(arucofound, img, drawId=True):

    if len(arucofound[0]) == 4:
        tl = (0, 0)
        tr = (0, 0)
        br = (0, 0)
        bl = (0, 0)

        for bbox, id in zip(arucofound[0], arucofound[1]):

            if id == 0:
                tl = bbox[0][0][0], bbox[0][0][1]
            elif id == 1:
                tr = bbox[0][1][0], bbox[0][1][1]
            elif id == 2:
                bl = bbox[0][3][0], bbox[0][3][1]
            elif id == 3:
                br = bbox[0][2][0], bbox[0][2][1]

        #h, w, c = imgAug.shape
        pts1 = np.array([tl, tr, br, bl])

        rotatedRect = cv2.minAreaRect(pts1)
        # Get rotated rect dimensions
        (x, y), (width, height), angle = rotatedRect
        # Get the 4 corners of the rotated rect
        # Top-left, top-right, bottom-right, bottom-left
        dstPts = [[0, 0], [width, 0], [width, height], [0, height]]
        # Get the transform
        m = cv2.getPerspectiveTransform(np.float32(pts1), np.float32(dstPts))
        # Transform the image
        out = cv2.warpPerspective(img, m, (int(width), int(height)))

        return out
    return img
