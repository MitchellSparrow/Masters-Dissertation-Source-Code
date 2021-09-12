import os
import asyncio
import cvb
import cv2
import numpy as np
import os
from globals import *
from helper import *
from robot_imports import *
from threading import Thread


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


def run_robot():

    keep_running = True

    logging.getLogger().setLevel(logging.INFO)

    conf = rtde_config.ConfigFile(CONFIG_FILENAME)
    state_names, state_types = conf.get_recipe('state')
    setp_names, setp_types = conf.get_recipe('setp')
    setg_names, setg_types = conf.get_recipe('setg')
    watchdog_names, watchdog_types = conf.get_recipe('watchdog')

    con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
    con.connect()

    # get controller version
    con.get_controller_version()

    print(con.get_controller_version())
    # setup recipes
    con.send_output_setup(state_names, state_types)
    setp = con.send_input_setup(setp_names, setp_types)
    setg = con.send_input_setup(setg_names, setg_types)
    watchdog = con.send_input_setup(watchdog_names, watchdog_types)

    setp.input_double_register_0 = 0
    setp.input_double_register_1 = 0
    setp.input_double_register_2 = 0
    setp.input_double_register_3 = 0
    setp.input_double_register_4 = 0
    setp.input_double_register_5 = 0

    # The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
    watchdog.input_int_register_0 = 0

    setg.input_int_register_1 = 0

    # start data synchronization
    if not con.send_start():
        sys.exit()

    print(setp_to_list(setp))

    try:
        while keep_running:
            print("STARTING PROGRAM")
            go_home(con, watchdog, setp)
            squeeze(con, watchdog, setp, setg)
            shake(con, watchdog, setp, setg)
            go_home(con, watchdog, setp)
            print("PROGRAM FINISHED")

    except KeyboardInterrupt:
        pass

    con.send_pause()
    con.disconnect()


def func2():
    print("hello")


if __name__ == "__main__":
    # run main loop
    port_0_points = calibrate_camera(0)
    port_1_points = calibrate_camera(1)
    loop = asyncio.get_event_loop()
    Thread(target=run_robot).start()
    Thread(target=loop.run_until_complete(asyncio.gather(async_acquire(
        0, port_0_points), async_acquire(
        1, port_1_points)))).start()
    
    # loop.run_until_complete(asyncio.gather(async_acquire(
    #     0, port_0_points), async_acquire(
    #     1, port_1_points)))
    loop.close()
    cv2.destroyAllWindows()
