import cv2
import cv2.aruco as aruco
import numpy as np
from globals import *
import cvb
import time


def find_contours(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(imgray, 100, 200, apertureSize=3)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(str(len(contours)))
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)


def configure_device(device: cvb.Device) -> None:
    dnode = device.node_maps['Device']
    dnode['Cust::autoBrightnessMode'].value = AUTO_BRIGHTNESS
    dnode['Std::BalanceWhiteAuto'].value = BALANCE_WHITE
    dnode['Std::AcquisitionFrameRate'].value = FPS
    dnode['Std::Width'].value = CAMERA_WIDTH
    dnode['Std::Height'].value = CAMERA_HEIGHT
    dnode['Std::OffsetX'].value = CAMERA_HORIZONTAL_OFFSET
    dnode['Std::OffsetY'].value = CAMERA_VERTICAL_OFFSET
    dnode['Std::TriggerMode'].value = 'Off'
    # dnode['Std::GevSCPSPacketSize'].value = 8192


def findArucoMarkers(img, markerSize=MARKER_SIZE, totalMarkers=50, draw=True):
    #img2 = np.array(img)
    #cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
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

# Robot controls


def setp_to_list(setp):
    list = []
    for i in range(0, 6):
        list.append(setp.__dict__["input_double_register_%i" % i])
    return list


def list_to_setp(setp, list):
    for i in range(0, 6):
        setp.__dict__["input_double_register_%i" % i] = list[i]
    return setp


# Wait and run
def new_move(con, watchdog, setp, target):

    target_pose = [round(p, 4) for p in target]
    list_to_setp(setp, target_pose)
    con.send(setp)
    start_time = time.time()

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > WHILE_LOOP_SECONDS:
            print("Could not reach position")
            break
        # receive the current state
        state = con.receive()
        actual_pose = [round(p, 4) for p in state.target_TCP_pose]

        if state is None or actual_pose == target_pose:
            break

        con.send(watchdog)


def new_grip(con, watchdog, setg, target_grip):

    setg.__dict__["input_int_register_1"] = target_grip
    con.send(setg)

    start_time = time.time()

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > WHILE_LOOP_SECONDS:
            print("Could not reach position")
            break
        # receive the current state
        state = con.receive()
        actual_grip = state.output_int_register_1

        if state is None or actual_grip == target_grip:
            break

        con.send(watchdog)


def go_home2(con, watchdog, setp):
    print("\tMoving to home position")
    new_move(con, watchdog, setp, home_pos)

def go_home(con, watchdog, setp):
    print("\tMoving to calibration position")
    new_move(con, watchdog, setp, calibration_pos)


def squeeze(con, watchdog, setp, setg):
    print("\tMoving to above grip position")
    new_move(con, watchdog, setp, above_grip_pos)
    print("\tMoving to grip position")
    new_move(con, watchdog, setp, grip_pos)
    print("\tOpen grip")
    new_grip(con, watchdog, setg, 1)
    print("\tClose grip")
    new_grip(con, watchdog, setg, 0)
    print("\tOpen grip")
    new_grip(con, watchdog, setg, 1)
    print("\tClose grip")
    new_grip(con, watchdog, setg, 0)
    print("\tOpen grip")
    new_grip(con, watchdog, setg, 1)
    print("\tMoving to above grip position")
    new_move(con, watchdog, setp, above_grip_pos)


def shake(con, watchdog, setp, setg):
    print("\tMoving to above grip position")
    new_move(con, watchdog, setp, above_grip_pos)
    print("\tMoving to grip position")
    new_move(con, watchdog, setp, grip_pos)
    print("\tClose grip")
    new_grip(con, watchdog, setg, 0)
    print("\tMoving to above grip position")
    new_move(con, watchdog, setp, above_grip_pos)
    print("\tMoving to shake 1 position")
    new_move(con, watchdog, setp, shake_1_pos)
    print("\tMoving to shake 2 position")
    new_move(con, watchdog, setp, shake_2_pos)
    print("\tMoving to shake 1 position")
    new_move(con, watchdog, setp, shake_1_pos)
    print("\tMoving to shake 2 position")
    new_move(con, watchdog, setp, shake_2_pos)
    print("\tMoving to above grip position")
    new_move(con, watchdog, setp, above_grip_pos)
    print("\tMoving to grip position")
    new_move(con, watchdog, setp, grip_pos)
    print("\tOpen grip")
    new_grip(con, watchdog, setg, 1)
    print("\tMoving to above grip position")
    new_move(con, watchdog, setp, above_grip_pos)
