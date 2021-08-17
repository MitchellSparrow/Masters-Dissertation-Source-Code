
import cvb
import cv2
import os
import numpy as np

FPS = 25
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_VERTICAL_OFFSET = 0
CAMERA_HORIZONTAL_OFFSET = 0
frameSize = (1920, 1080)


def configure_device(device: cvb.Device) -> None:
    dnode = device.node_maps["Device"]
    dnode['Cust::autoBrightnessMode'].value = 'Active'  # Can be Off
    dnode['Std::BalanceWhiteAuto'].value = 'OnDemand'
    # dnode['Std::AcquisitionFrameRate'].value = FPS
    # dnode['Std::Width'].value = CAMERA_WIDTH
    # dnode['Std::Height'].value = CAMERA_HEIGHT
    # dnode['Std::OffsetX'].value = CAMERA_HORIZONTAL_OFFSET
    # dnode['Std::OffsetY'].value = CAMERA_VERTICAL_OFFSET
    # dnode['Std::TriggerMode'].value = 'Off'
    #dnode['Std::GevSCPSPacketSize'].value = 8192


# with cvb.DeviceFactory.open(
#         os.path.join(cvb.install_path(), "Drivers", "CVMock.vin"),
#         cvb.AcquisitionStack.Vin) as device:

    # # load the correct driver for the device
driver = os.path.join(cvb.install_path(), 'Drivers', 'GenICam.vin')
# # load the correct device
# device = cvb.DeviceFactory.open(driver, port=0)

with cvb.DeviceFactory.open(driver, port=0) as device:

    configure_device(device)

    stream = device.stream()
    stream.start()

    try:
        while True:

            image, status = stream.wait()

            if status == cvb.WaitStatus.Ok:
                # np_image = cvb.as_array(image, copy=False)
                # cv2.imshow('Network Camera',  cv2.resize(
                #     np_image, (800, 600)))
                #image_np = np.array(frame)
                image_np = cvb.as_array(image, copy=False)
                #image_np = np.array(image)

                cv2.imshow('Network Camera',  cv2.resize(
                    image_np, (800, 600)))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            else:
                raise RuntimeError("timeout during wait"
                                   if status == cvb.WaitStatus.Timeout else
                                   "acquisition aborted")
    except KeyboardInterrupt:
        stream.try_abort()

    finally:
        stream.try_abort()
