# CVBpy Example Script
#
# 1. Discover all devices.
# 2. Load the first device found.
# 3. Acquire images.
#

# https://help.commonvisionblox.com/API/Python/cvb_2_discover_devices-example.html

import cvb
import cv2
import os

discover = cvb.DeviceFactory.discover_from_root()

mock_info = next(
    (info for info in discover if "CVMock.vin" in info.access_token), None)
if mock_info is None:
    raise RuntimeError("unable to find CVMock.vin")

# load the device
driver = os.path.join(cvb.install_path(), 'Drivers', 'GenICam.vin')
# print(cvb.install_path())
device = cvb.DeviceFactory.open(driver, port=0)

with cvb.DeviceFactory.open(driver, port=0) as device:

    # with cvb.DeviceFactory.open(
    #         mock_info.access_token, cvb.AcquisitionStack.Vin) as device:

    stream = device.stream()
    stream.start()

    for i in range(10):
        image, status = stream.wait()
        if status == cvb.WaitStatus.Ok:
            print("Acquired image: " + str(i))
            # print(type(image))
            np_array = cvb.as_array(image, copy=False)
            cv2.imshow('Network Camera',  cv2.resize(
                np_array, (800, 600)))

    stream.abort()
