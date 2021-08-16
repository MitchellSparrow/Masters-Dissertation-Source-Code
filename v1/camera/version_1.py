
import cv2
import numpy as np


cap = cv2.VideoCapture('rtsp://10.1.6.94', cv2.CAP_DSHOW)
# cap = cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')

# cap = cv2.VideoCapture('rtsp://S1218343:password@10.1.6.98/1')

# Setup capture
#cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


while True:
    ret, frame = cap.read()
    image_np = np.array(frame)

    cv2.imshow('Network Camera',  cv2.resize(
        image_np, (800, 600)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break


cv2.destroyAllWindows()
