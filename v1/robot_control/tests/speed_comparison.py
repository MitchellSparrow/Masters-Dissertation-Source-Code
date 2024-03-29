
from tensorflow import keras
import time
import numpy as np
import cv2
import segmentation_models as sm
import tensorflow as tf

# sm.set_framework('tf.keras')
# sm.framework()
backbone = "resnet34"

# model = sm.Unet(BACKBONE, encoder_weights="imagenet")
# model.compile('Adam', loss = sm.losses.bce_jaccard_loss,metrics=[sm.metrics.iou_score])

preprocess_input = sm.get_preprocessing(backbone)


FRAME_SIZE = (640, 480)
model = keras.models.load_model('complete_program/models/my_model_10.h5', compile=False)

cap = cv2.VideoCapture(0)

def get_masked_image( image):
    res = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    start = time.time()
    res = preprocess_input(res)
    res = np.expand_dims(res, 0)
    prediction = (model.predict(res)[0,:,:,0] > 0.2).astype(np.uint8)*255
    end = time.time()

    redImg = np.zeros(image.shape, image.dtype)
    redImg[:,:] = (0, 0, 255)
    redMask = cv2.bitwise_and(redImg, redImg, mask=prediction)
    added_image = cv2.addWeighted(image,1.0,redMask,0.5,0)
    added_image = cv2.resize(added_image, FRAME_SIZE)

    print(f"Prediction: {end - start}")
    return added_image

while True:
    ret, frame = cap.read()
    result = get_masked_image(frame)
    cv2.imshow('Instance Segmentation', result)
    
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Instance Segmentation',4)<1:
        cv2.destroyAllWindows()
        break