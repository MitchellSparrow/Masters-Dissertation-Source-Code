import time
import os
import cvb
import cvb.ui

import cv2

FPS = 2
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_VERTICAL_OFFSET = 0
CAMERA_HORIZONTAL_OFFSET = 0
frameSize = (700, 500)


def configure_device(device: cvb.Device) -> None:
    dnode = device.node_maps['Device']
    dnode['Cust::autoBrightnessMode'].value = 'Active'  # Can be Off
    dnode['Std::BalanceWhiteAuto'].value = 'OnDemand'
    dnode['Std::AcquisitionFrameRate'].value = FPS
    #dnode['Std::Width'].value = CAMERA_WIDTH
    #dnode['Std::Height'].value = CAMERA_HEIGHT
    # dnode['Std::OffsetX'].value = CAMERA_HORIZONTAL_OFFSET
    # dnode['Std::OffsetY'].value = CAMERA_VERTICAL_OFFSET
    #dnode['Std::TriggerMode'].value = 'Off'
    # dnode['Std::GevSCPSPacketSize'].value = 8192


class MyStreamHandler(cvb.SingleStreamHandler):

    def __init__(self, stream, port):
        super().__init__(stream)
        self.rate_counter = cvb.RateCounter()
        self.port = port

    # called in the interpreter thread to setup additionla stuff.
    def setup(self, stream):
        super().setup(stream)
        print("setup")

    # called in the interpreter thread to tear down stuff from setup.
    def tear_down(self, stream):
        super().tear_down(stream)
        print("tear_down")

    # called from the aqusition thread
    def handle_async_stream(self, stream):
        super().handle_async_stream(stream)
        # print("handle_async_stream")

    # called from the aqusition thread
    def handle_async_wait_result(self, image, status):
        super().handle_async_wait_result(image, status)
        # self.rate_counter.step()

        image_np = cvb.as_array(image, copy=False)

        # rate_counter.step()
        if status == cvb.WaitStatus.Ok:

            cv2.imshow(str(self.port),  cv2.resize(
                cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR), (700, 500)))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

        else:
            raise RuntimeError("timeout during wait"
                               if status == cvb.WaitStatus.Timeout else
                               "acquisition aborted")

        # print("New image: " + image.__class__.__name__ + " " + str(image) +
        #       " | Status: " + str(status) + " | Buffer Index: " + str(image.buffer_index))

    # print messurement results
    def eval(self):
        print("Acquired with: " + str(self.rate_counter.rate) + " fps")


with cvb.DeviceFactory.open(
        os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'),
        port=0) as cam0, cvb.DeviceFactory.open(
        os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'),
        port=1) as cam1:
    configure_device(cam0)
    configure_device(cam1)
    with MyStreamHandler(cam0.stream(), 0) as handler0, MyStreamHandler(cam1.stream(), 1) as handler1:

        handler0.run()
        handler1.run()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            handler0.finish()
            handler1.finish()


cv2.destroyAllWindows()
