#!/bin/bash

# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade

# Install Python 3.8 and set it to path
sudo apt-get install python3.8
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# Install raspi-config
sudo apt-get install -y raspi-config

# Enable camera and GPIO pins using raspi-config
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_serial 0

# Install modules for controlling ultrasonic sensor, servo motor, and DC motor
sudo apt-get install python3-gpiozero
sudo apt-get install python3-pigpio
sudo apt-get install python3-picamera
sudo apt-get install python3-opencv
sudo apt-get install python3-numpy
sudo apt-get install python3-scipy
sudo apt-get install python3-pandas
sudo apt-get install python3-matplotlib
sudo apt-get install python3-tk
sudo apt-get install python3-serial

# Set up the Coral USB accelerator
cd ~
wget https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz -O edgetpu_api_latest.tar.gz
tar xzf edgetpu_api_latest.tar.gz
cd edgetpu_api
bash ./install.sh

# # Compile the YOLOv5s model to work with the Coral accelerator
# cd ~
# git clone https://github.com/ultralytics/yolov5.git
# cd yolov5
# sudo apt-get install protobuf-compiler libprotoc-dev
# sudo pip install -r requirements.txt
# python models/export.py --weights yolov5s.pt --img 640 --batch 1 --include package='edgetpu' --include file=tflite_convert
