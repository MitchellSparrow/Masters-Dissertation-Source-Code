
import os
import asyncio
import cvb
import cv2
import numpy as np
import os
from globals import *
from helper import *


async def async_acquire(port, points):
    with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'), port=port) as device:
        configure_device(device)
        stream = device.stream()
        stream.start()
        image_name = 'Port ' + str(port)

        while True:
            result = await stream.wait_async()
            image, status = result.value
            img = transform_image(image, points)

            if status == cvb.WaitStatus.Ok:
                cv2.imshow(image_name, cv2.resize(
                    cv2.cvtColor(img, cv2.COLOR_RGB2BGR), FRAME_SIZE))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                raise RuntimeError("timeout during wait"
                                   if status == cvb.WaitStatus.Timeout else
                                   "acquisition aborted")

        stream.try_abort()


def calibrate_camera(port):
    with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'), port=port) as device:
        configure_device(device)
        stream = device.stream()
        image_name = 'Port ' + str(port)
        points = np.zeros([4, 2])
        stream.start()

        # First find the aruco images and save the points to an array
        while not points.any():

            image, status = stream.wait()
            arucofound = findArucoMarkers(image)
            points = find_points(arucofound, image)

            if status == cvb.WaitStatus.Ok:
                image_np = cvb.as_array(image, copy=False)
                cv2.imshow(image_name, cv2.resize(
                    cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR), FRAME_SIZE))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

        stream.try_abort()
        return points


if __name__ == "__main__":
    # run main loop
    port_1_points = calibrate_camera(1)
    # port_0_points = calibrate_camera(0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(async_acquire(1, port_1_points)))
    loop.close()
    cv2.destroyAllWindows()
