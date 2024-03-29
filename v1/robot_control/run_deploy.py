import os
import cvb
import cv2
import numpy as np
import os
from globals import *
from helper import *
from robot_imports import *
import uuid 
from tensorflow import keras
import time
import multiprocessing
import segmentation_models as sm

class Run:
    def __init__(self):
        
        self.record = multiprocessing.Event()
        self.collect_lstm_data = True
        self.stream_queues = []
        self.path_cam = os.getcwd() + "\\new_data\\new_images\\"
        print(self.path_cam)

        self.preprocess_input = sm.get_preprocessing(BACKBONE)

        # recording data 
        self.action = 0
        self.sequence = 0
        self.frame_num = 0

        if self.collect_lstm_data:
            self.setup_video_directories()

        for i in range(NUM_CAMERAS):
            self.stream_queues.append(multiprocessing.Queue())

        self.exit = multiprocessing.Event()

        self.lstm_buffer = []

        self.keep_running = True
        self.calibrating = True
        self.stream_images = []

        for i in range(NUM_CAMERAS):
            self.stream_images.append(np.zeros((FRAME_SIZE[1],FRAME_SIZE[0],3), np.uint8))

        #  UNCOMMENT     
        self.calibration_points = []
        for i in range(NUM_CAMERAS):
            self.calibration_points.append(self.calibrate_camera(i))

    def run(self):
        # Create a list of processes that we want to run at the same time        
        multiprocess = []

        # UNCOMMENT 
        multiprocess.append(multiprocessing.Process(None,self.stream_camera_mp,args=[self.stream_queues[1],1,self.calibration_points[1]]))
        multiprocess.append(multiprocessing.Process(None,self.stream_camera_mp,args=[self.stream_queues[0],0,self.calibration_points[0]]))

        # COMMENT
        # self.record.set()
        # multiprocess.append(multiprocessing.Process(None,self.stream_camera2_mp,args=[self.stream_queues[1],]))

        # add the robot control process
        # UNCOMMENT 
        multiprocess.append(multiprocessing.Process(None,self.run_robot))
        
        for p in multiprocess:
            p.daemon = True

        for x in multiprocess:
            x.start()
            time.sleep(1)
        
        # [x.start() for x in multiprocess]
        
        self.model = keras.models.load_model('models/my_model_18.h5', compile=False)
        self.display_masked_images_mp()
        #self.display_images_mp()
        #self.save_images()
        

    def save_images(self):
        while not self.exit.is_set():
            cv_image = np.concatenate((self.stream_queues[0].get(), self.stream_queues[1].get()), axis=1)
            if cv_image is None:  continue  

            cv2.imwrite(os.path.join(self.path_cam, '{}.jpg'.format(str(uuid.uuid1()))), self.stream_queues[0].get())
            cv2.imwrite(os.path.join(self.path_cam, '{}.jpg'.format(str(uuid.uuid1()))), self.stream_queues[1].get())

            cv2.imshow('Instance Segmentation', cv_image)

            cv2.waitKey(1000)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Instance Segmentation',4)<1:
                cv2.destroyAllWindows()
                self.exit.set()


    def display_images(self):
        while self.keep_running:
            cv_image = np.concatenate((self.stream_images[0], self.stream_images[1]), axis=1)
            cv2.imshow('Instance Segmentation', cv_image)
            
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Instance Segmentation',4)<1:
                cv2.destroyAllWindows()
                self.keep_running = False

    def display_masked_images(self):
        while self.keep_running:
            image_1 = self.get_masked_image(self.stream_images[0])[0]
            image_2 = self.get_masked_image(self.stream_images[1])[0]
            cv_image = np.concatenate((cv2.resize(image_1, (320,480)), cv2.resize(image_2, (320,480))), axis=1)
            #cv_image = np.concatenate((image_1,image_2), axis=1)
            cv2.imshow('Instance Segmentation', cv_image)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Instance Segmentation',4)<1:
                cv2.destroyAllWindows()
                self.keep_running = False


    def display_images_mp(self):
        while not self.exit.is_set():
            cv_image = np.concatenate((self.stream_queues[0].get(), self.stream_queues[0].get()), axis=1)
            if cv_image is None:  continue             
        
            cv2.imshow('Instance Segmentation', cv_image)
            
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Instance Segmentation',4)<1:
                cv2.destroyAllWindows()
                self.exit.set()

    def display_masked_images_mp(self):
        while not self.exit.is_set():
            image_1_result = self.get_masked_image(self.stream_queues[1].get())
            image_1 = image_1_result[0]
            #image_2 = self.get_masked_image(self.stream_queues[0].get())[0]
            image_2 = self.stream_queues[1].get()
            cv_image = np.concatenate((image_1, image_2), axis=1)

            if cv_image is None: continue

            if self.collect_lstm_data:
                cv2.putText(cv_image, 'Collecting frames for {} Video Number {}, frame: {} Recording: {}'.format(SPONGE_CLASSIFICATIONS[self.action], self.sequence, self.frame_num, self.record.is_set()), (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
            cv2.imshow('Instance Segmentation', cv_image)

            if self.record.is_set(): 
                if self.collect_lstm_data:
                    self.save_video_data(image_1_result[1])

                    if self.frame_num == SEQUENCE_LENGTH - 1:
                        if self.sequence == NO_SEQUENCES - 1:
                            if self.action == len(SPONGE_CLASSIFICATIONS) - 1:
                                self.collect_lstm_data = False
                            else:
                                self.action += 1
                            self.sequence = 0
                        else:
                            self.sequence += 1
                        self.frame_num = 0
                        self.record.clear()
                    else:
                        self.frame_num += 1
                else:
                    self.lstm_buffer.append(image_1_result[1].flatten())
                    if self.frame_num == SEQUENCE_LENGTH - 1:
                        self.run_lstm_prediction()
                        self.frame_num = 0
                        self.record.clear()
                    else:
                        self.frame_num += 1



            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Instance Segmentation',4)<1:
                cv2.destroyAllWindows()
                self.exit.set()

    def setup_video_directories(self):
        for classification in SPONGE_CLASSIFICATIONS:
            for sequence in range(NO_SEQUENCES):
                try:
                    os.makedirs(os.path.join('LSTM_Data/', classification, str(sequence)))
                except:
                    pass

    def save_video_data(self, detections):
        npy_path = os.path.join(
                'LSTM_Data/', SPONGE_CLASSIFICATIONS[self.action], str(self.sequence), str(self.frame_num))
        np.save(npy_path, detections)
        

    def get_masked_image(self, image):
        res = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        start = time.time()
        res = self.preprocess_input(res)
        res = np.expand_dims(res, 0)
        prediction = (self.model.predict(res)[0,:,:,0] > SEM_SEG_THRESH).astype(np.uint8)*255
        end = time.time()
        redImg = np.zeros(image.shape, image.dtype)
        redImg[:,:] = (0, 0, 255)
        redMask = cv2.bitwise_and(redImg, redImg, mask=prediction)
        added_image = cv2.addWeighted(image,1.0,redMask,0.5,0)
        added_image = cv2.resize(added_image, FRAME_SIZE)
        #print(end - start)
        return [added_image, prediction/255]


    def stream_camera(self, port, points):
        with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'), port=port) as device:
            configure_device(device)
            stream = device.stream()
            stream.start()

            while self.keep_running:
                image, status = stream.wait()

                if status == cvb.WaitStatus.Ok:
                    image_np = cvb.as_array(image, copy=False)
                    self.stream_images[port] = cv2.resize(cv2.cvtColor(transform_image(image_np, points), cv2.COLOR_RGB2BGR), FRAME_SIZE)
                    
                else:
                    raise RuntimeError("timeout during wait"
                                    if status == cvb.WaitStatus.Timeout else
                                    "acquisition aborted")

            stream.try_abort()

    def stream_camera2(self,port):
        cap = cv2.VideoCapture(0)
        while self.keep_running:
            ret, frame = cap.read()
            result = self.get_masked_image(frame)[0]
            self.stream_images[port] = result

    def stream_camera_mp(self,q,port,points):
        with cvb.DeviceFactory.open(os.path.join(cvb.install_path(), "drivers", 'GenICam.vin'), port=port) as device:
            configure_device(device)
            stream = device.stream()
            stream.start()

            while not self.exit.is_set():
                image, status = stream.wait()

                if status == cvb.WaitStatus.Ok:
                    image_np = cvb.as_array(image, copy=False)
                    q.put(cv2.resize(cv2.cvtColor(transform_image(image_np, points), cv2.COLOR_RGB2BGR), FRAME_SIZE))
                    
                else:
                    raise RuntimeError("timeout during wait"
                                    if status == cvb.WaitStatus.Timeout else
                                    "acquisition aborted")

            stream.try_abort()


    def stream_camera2_mp(self,q):
        cap = cv2.VideoCapture(0)
        while not self.exit.is_set():
            ret, frame = cap.read()
            q.put(frame)


    def calibrate_camera(self, port):
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
                    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(image_name,4)<1:
                        cv2.destroyAllWindows()
                        break

            stream.try_abort()
            cv2.destroyAllWindows()
            return points       


    def run_lstm_prediction(self):
        pass



    def run_robot(self,):

        logging.getLogger().setLevel(logging.INFO)

        conf = rtde_config.ConfigFile(CONFIG_FILENAME_DEPLOY)
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
            while self.keep_running:
                print("STARTING PROGRAM")
                go_home(con, watchdog, setp)
                before_squeeze(con, watchdog, setp, setg)
                self.record.set()
                squeeze(con, watchdog, setp, setg)
                before_squeeze(con, watchdog, setp, setg)
                # self.record.clear()
                # shake(con, watchdog, setp, setg)
                go_home(con, watchdog, setp)
                print("PROGRAM FINISHED")

        except KeyboardInterrupt:
            pass

        con.send_pause()
        con.disconnect()

def test():
        print("try")

if __name__ == "__main__":

    run = Run()
    run.run()
   