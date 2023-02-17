#!/bin/bash

# Update package list and upgrade existing packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages for Python and Coral USB Accelerator
sudo apt-get install python3 python3-pip python3-edgetpu libedgetpu1-std libedgetpu-dev -y

# Install required packages for PWM control
sudo apt-get install pigpio -y

# Enable the I2C and SPI interfaces
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0

# Install the pigpio library for Python
sudo pip3 install pigpio

# Install the RPi.GPIO library for Python
sudo pip3 install RPi.GPIO

# Install the numpy and opencv-python libraries for Python
sudo pip3 install numpy opencv-python

# Download and install the Ultrasonic Sensor driver
cd ~
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python3 setup.py install

# Download and install the YOLOv5 model for object detection
cd ~
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
sudo pip3 install -r requirements.txt
python3 detect.py --weights yolov5s.pt --img 640 --conf 0.4 --source 0

# Download and install the pycoral library for the Coral USB Accelerator
cd ~
wget https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl
sudo pip3 install tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl

sudo apt-get install edgetpu-compiler
