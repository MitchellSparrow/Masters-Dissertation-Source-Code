# Overview:

There are three main scripts which can be run in this folder. The first is to collect data, and the second is to deploy code onto a remote server, and the third is to run the main program on the remote server. The details of these scripts are outlined below:

## a.) Collect images:

Run the following code on your local machine.

```
python collect_images_2.py
```

## b.) Deploy code onto remote server:

Run the following code on your local machine. This loops through all of the files and directories in the chosen directory to copy.

```
python deploy.py
```

## c.) Run the main program:

Run the following code on the REMOTE SERVER (as this will be much faster than a standard computer).

```
python runDeploy.py
```

# Folder and file structure / notes

* The Real-Time Data Exchange (RTDE) folder is the main RTDE library
* The examples folder contains some basic, public examples of the RTDE library
* The globals file is just a list of parameters used for the cameras and other functions

# Other notes

## Transfer files to and from remote server using PSCP

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







