import os
import asyncio
import cvb
import cv2

rate_counter = None

FPS = 10
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_VERTICAL_OFFSET = 0
CAMERA_HORIZONTAL_OFFSET = 0
frameSize = (1920, 1080)


def configure_device(device: cvb.Device) -> None:
    dnode = device.node_maps['Device']
    dnode['Cust::autoBrightnessMode'].value = 'Active'  # Can be Off
    #dnode['Std::BalanceWhiteAuto'].value = 'OnDemand'
    dnode['Std::AcquisitionFrameRate'].value = FPS
    #dnode['Std::Width'].value = CAMERA_WIDTH
    #dnode['Std::Height'].value = CAMERA_HEIGHT
    #dnode['Std::OffsetX'].value = CAMERA_HORIZONTAL_OFFSET
    #dnode['Std::OffsetY'].value = CAMERA_VERTICAL_OFFSET
    #dnode['Std::TriggerMode'].value = 'Off'
    #dnode['Std::GevSCPSPacketSize'].value = 8192


async def async_acquire(port):
    global rate_counter
    with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'), port=port) as device:
        configure_device(device)
        stream = device.stream()
        stream.start()

        rate_counter = cvb.RateCounter()

        while True:
            result = await stream.wait_async()
            image, status = result.value
            rate_counter.step()
            if status == cvb.WaitStatus.Ok:

                image_np = cvb.as_array(image, copy=False)

                cv2.imshow('Port ' + str(port),
                           cv2.resize(image_np, (700, 500)))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            else:
                raise RuntimeError("timeout during wait"
                                   if status == cvb.WaitStatus.Timeout else
                                   "acquisition aborted")

        stream.try_abort()


def main_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(async_acquire(0), async_acquire(1)))
    loop.close()


# Run main loop
main_loop()
