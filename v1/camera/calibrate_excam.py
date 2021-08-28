import os
import asyncio
import cvb
import cv2
import numpy as np
import os
from globals import *
from helper import *


# import pixellib
# from pixellib.instance import instance_segmentation
# import cv2

# from pixellib.instance import custom_segmentation

# segmentation_model = custom_segmentation()
# segmentation_model.inferConfig(num_classes=1, class_names=["BG", "Object"])
# segmentation_model.load_model("camera/models/mask_rcnn_model.019-0.155671.h5")


#segmentation_model = instance_segmentation(infer_speed="fast")
# segmentation_model.load_model('camera/models/mask_rcnn_coco.h5')


async def async_acquire(port, points):
    with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'), port=port) as device:
        configure_device(device)
        stream = device.stream()
        stream.start()
        image_name = 'Port ' + str(port)

        while True:
            result = await stream.wait_async()
            image, status = result.value

            if status == cvb.WaitStatus.Ok:
                image_np = cvb.as_array(image, copy=False)
                img = transform_image(image_np, points)
                # find_contours(image_np)
                # res = segmentation_model.segmentFrame(img, show_bboxes=True)
                # image_res = res[1]

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
        points = np.zeros([4, 2])
        configure_device(device)
        stream = device.stream()
        image_name = 'Port ' + str(port)

        stream.start()

        # First find the aruco images and save the points to an array
        while not points.any():

            image, status = stream.wait()

            if status == cvb.WaitStatus.Ok:
                image_np = cvb.as_array(image, copy=False)
                arucofound = findArucoMarkers(image_np)
                # print(arucofound)
                points = find_points(arucofound, image)

                cv2.imshow(image_name, cv2.resize(
                    cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR), FRAME_SIZE))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

        stream.try_abort()
        return points


if __name__ == "__main__":
    # run main loop
    port_0_points = calibrate_camera(0)
    port_1_points = calibrate_camera(1)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(async_acquire(
        0, port_0_points), async_acquire(
        1, port_1_points)))
    loop.close()
    cv2.destroyAllWindows()
