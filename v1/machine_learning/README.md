# Machine Learning Code

The following folder contains the two main machine learning elements to the project, being the semantic segmentation model and the LSTM model.

The following image shows a flow diagram of the full machine learning pipeline used to predict the physical properties of objects. The input images from a video camera are first fed into the image segmentation model before being passed as a series into the time series model (LSTM) which makes the final prediction on the physical properties of the object

![alt text](https://i.imgur.com/kbv6Ovb.png)

# Google colab

We recommend that you pay for Colab Pro if you are training any models in the cloud, however if you want to train a model as a once off, here is a nifty trick to keep the free version of google colab active in your browser:

## How to keep google colab (free version) active in your browser

Run the following code in the browser console:

```
function ClickConnect(){
console.log("Working");
document.querySelector("colab-connect-button").shadowRoot.getElementById('connect').click();
}
setInterval(ClickConnect,60000) 
```

# Remote server machine learning setup
To check if the GPU's are running run the following python commands 

```
import tensorflow as tf
```
Once tensorflow is installed, run the following command to make sure it is running on the GPU's
```
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
```
