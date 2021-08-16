import cv2
import cvb
import numpy as np

# Camera settings
CAMERA_EXPOSURE = 7000
if __name__ == '__main__':
    vin_device = cvb.DeviceFactory.open(
        cvb.install_path() + "/drivers/GenICam.vin")
    vin_device.stream.ring_buffer.change_count(1, 0)
    dev_node_map = vin_device.node_maps["Device"]
    exposure_node = dev_node_map["ExposureTime"]
    exposure_node.value = CAMERA_EXPOSURE
    stream = vin_device.stream
    stream.start()
    try:
        while True:
            trigger = input('Press o to acquire: ')
            if trigger == 'o':
                trigger = ''

                for ii in range(0, 2):  # I use this method to empty the ring buffer
                    image, status = stream.wait()
                np_image = cvb.as_array(image, copy=False)
                cv2.imwrite('image_' + str(0) + '.png', np_image)
                if status == cvb.WaitStatus.Ok:
                    print("Acquired image " + " into buffer " +
                          str(image.buffer_index) + ".")
                else:
                    raise RuntimeError("timeout during wait"
                                       if status == cvb.WaitStatus.Timeout else
                                       "acquisition aborted")
    except KeyboardInterrupt:
        pass

    finally:
        stream.try_abort()
