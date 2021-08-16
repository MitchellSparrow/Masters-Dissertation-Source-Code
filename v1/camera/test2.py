import os
import cvb
import cv2
FPS = 25
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_VERTICAL_OFFSET = 32
CAMERA_HORIZONTAL_OFFSET = 32
frameSize = (1920, 1080)


def deviceConfiguration(dev_node_map):
    dev_node_map['Std::Width'].value = CAMERA_WIDTH
    dev_node_map['Std::Height'].value = CAMERA_HEIGHT
    # set the Frame rate in Hz
    dev_node_map['Std::AcquisitionFrameRate'].value = FPS
    dev_node_map['Std::OffsetX'].value = CAMERA_HORIZONTAL_OFFSET
    dev_node_map['Std::OffsetY'].value = CAMERA_VERTICAL_OFFSET
    dev_node_map['Cust::autoBrightnessMode'].value = "Active"


if __name__ == '__main__':
    rate_counter = None
    out = cv2.VideoWriter(
        'recording.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25, frameSize)
    with cvb.DeviceFactory.open(cvb.install_path() + "/drivers/GenICam.vin", port=0) as device:
        deviceConfiguration(device.node_maps["Device"])
        device.node_maps["Device"]['Cust::timestampControlLatch'].execute()
        stream = device.stream
        rate_counter = cvb.RateCounter()

        stream.start()
        for i in range(10):
            rate_counter.step()
            image, status = stream.wait()
            if status == cvb.WaitStatus.Ok:
                np_image = cvb.as_array(image, copy=False)
                # save the frames
                out.write(np_image)
                imageRawTimeStamp = "{:.0f}".format(float(image.raw_timestamp))
