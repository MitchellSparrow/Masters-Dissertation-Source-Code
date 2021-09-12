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

#https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread