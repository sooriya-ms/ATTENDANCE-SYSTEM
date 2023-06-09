# ATTENDANCE-SYSTEM

This project is built to maintain the arrival and departure times for the attendance system in a cloud database. It uses Face Recognition to capture and verify the people. It's specifically made to run the real-time face capturing in Raspberry PI. Which is a minimal hardware setup to capture and analyse.

## Overview

Before real-time capturing, the initial face data for training can be uploaded to the webpage. This webpage is made with DJango. Which have an authentication page. After the authentication, the authorised person can upload the image, name, email, phone number, etc. This will add these data to the SQL database.

Now, to train the Deep Learning model, the webpage contains a button labelled __"Train Model"__. Whenever this button is triggered, the model is trained and sent to all the Raspberry PI devices automatically if both the server and Raspberry PIs are connected to the same WiFi network. Which is done by WebSockets.

The python code in Raspberry PI is running continuously. Whenever a new model is trained with new images, it immediately reflects all the Raspberry Pis. We don't need to re-run the Python code on the edge devices. The in-time and out-time of the person will be stored in the __Real-Time Database Firebase__. _There is a restriction/feature :_ only after five minutes of in-time is the out-time noted.

## Setup

To run this program, we need to install all the required libraries, such as DJango, openCV, dlib, cmake, firebase_admin, face_recognition, etc. Then run the Django application using `python manage.py runserver`.<br />
The 'realtime.py' file is placed inside the Edge Node devices. Other files, which are DJango files, must be placed on the server.

## Features

* Arrival captured in one node, and departure is captured in another node.
* Recognise more than one face at a time.
* Immediate Cloud Storage
* The minimum time after arrival to depart is 5 minutes.

## Screenshots

![Login Page](https://github.com/sooriya-ms/ATTENDANCE-SYSTEM/blob/master/ScreenShot/authentication.png)
<br />
![Upload Page](https://github.com/sooriya-ms/ATTENDANCE-SYSTEM/blob/master/ScreenShot/upload_page.png)
<br />
