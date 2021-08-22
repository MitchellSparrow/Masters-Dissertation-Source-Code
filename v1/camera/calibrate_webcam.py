import cv2
import numpy as np
from globals import *
from helper import *


def main():
    # Create video capture
    cap = cv2.VideoCapture(0)
    points = np.zeros([4, 2])

    # First find the aruco images and save the points to an array
    while not points.any():
        success, img = cap.read()
        arucofound = findArucoMarkers(img)

        img = arucoAug(arucofound, img)
        points = find_points(arucofound, img)

        cv2.imshow('Calibrating...', cv2.resize(
            img, FRAME_SIZE))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Now we need to release the current window and create a new one
    cap.release()
    cap = cv2.VideoCapture(0)

    # Now that we have the aruco points, we can stream and transform the image
    while True:

        success, img = cap.read()

        img = transform_image(img, points)

        cv2.imshow('img', cv2.resize(
            img, (800, 600)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cap.destroyAllWindows()


if __name__ == "__main__":
    main()
