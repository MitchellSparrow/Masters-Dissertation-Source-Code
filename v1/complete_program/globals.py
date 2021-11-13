import numpy as np

NUM_CAMERAS = 2
MARKER_SIZE = 6
FPS = 10
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 900
CAMERA_VERTICAL_OFFSET = 320
CAMERA_HORIZONTAL_OFFSET = 400
FRAME_SIZE = (640, 480)

AUTO_BRIGHTNESS = 'Active'  # can be active or off
BALANCE_WHITE = 'OnDemand'

WHILE_LOOP_SECONDS = 5

#ROBOT_HOST = '192.168.86.128'
ROBOT_HOST = '10.0.1.1'
ROBOT_PORT = 30004
CONFIG_FILENAME = 'complete_program/robot_configuration.xml'
CONFIG_FILENAME_DEPLOY = 'robot_configuration.xml'

## LSTM VIDEO COLLECTION PARAMETERS:

SPONGE_CLASSIFICATIONS = np.array(['no_object', 'soft', 'medium', 'firm', 'very_firm'])
# 15 videos worth of data
NO_SEQUENCES = 15
# Each video is 30 frames long
SEQUENCE_LENGTH = 20
# Threshold over which to draw sematic segmentation 
SEM_SEG_THRESH = 0.2

## ROBOT PARAMETERS

setp1 = [-0.129, -0.322, -0.05, -0.022, -1.603, -0.034]
setp2 = [-0.25, -0.322, -0.05, -0.022, -1.603, -0.034]


calibration_pos = [-0.068, -0.2809, 0.1961, 2.2827, 2.1357, -0.0262]
grip_pos = [-0.25, -0.322, -0.155, -0.022, -1.603, -0.034]
above_grip_pos = [-0.25, -0.322, -0.1, -0.022, -1.603, -0.034]
home_pos = [-0.129, -0.322, -0.1, -0.022, -1.603, -0.034]
shake_1_pos = [-0.2426, -0.2607, -0.102, -0.1513, -1.6037, -0.1677]
shake_2_pos = [-0.2466, -0.3875, -0.0976, 0.1153, -1.5933, 0.1079]
