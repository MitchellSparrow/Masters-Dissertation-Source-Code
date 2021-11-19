Real-Time Data Exchange (RTDE) python client + examples

rtde - main RTDE library
examples - Examples showing basic use cases for the RTDE

# Remote server connection:

https://stackoverflow.com/questions/20499074/run-local-python-script-on-remote-server

# Google colab
## How to keep it running

Run the following code in the browser console:

```
function ClickConnect(){
console.log("Working");
document.querySelector("colab-connect-button").shadowRoot.getElementById('connect').click();
}
setInterval(ClickConnect,60000) 
```

# Multiprocessing and multithread sources

https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread

# Copy files to remote server using PSCP

```
pscp -P 22 demo-file.zip mitchellsparrow@gerty.cobotmakerspace.org:/root/
```
Transfer from remote server to the host machine:
must be in the directory where you want the file to be 
```
pscp -P 22 mitchellsparrow@gerty.cobotmakerspace.org:/home/mitchellsparrow/tmp/complete_program/LSTM_Data lstm-data
```
This works for directories:
```
scp -r 22 mitchellsparrow@gerty.cobotmakerspace.org:/home/mitchellsparrow/tmp/complete_program/LSTM_Data .
```

# To check if the GPU's are running run the following python commands 

```
import tensorflow as tf
```
and then:
```
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
```