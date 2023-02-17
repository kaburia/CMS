#!/bin/bash

# Install and setup Python3.8
sudo apt update
sudo apt install -y python3.8
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
sudo update-alternatives --set python /usr/bin/python3.8

# Install necessary packages
sudo apt install -y python3-pip python3-opencv libopencv-dev libjasper-dev libqtgui4 libqt4-test libhdf5-dev libhdf5-103 libatlas-base-dev libjasper-dev libqtgui4 libqt4-test libilmbase-dev libopenexr-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libtbb-dev libdc1394-22-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libopenblas-dev

# Install pip packages
sudo pip3 install numpy pandas matplotlib scikit-learn scipy imutils pillow tensorflow keras pycoral RPi.GPIO adafruit-blinka

# Enable SPI and I2C interfaces
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0

# Clone YOLOv5 repository
git clone https://github.com/ultralytics/yolov5.git
cd yolov5

# Install YOLOv5 dependencies
sudo pip3 install -r requirements.txt

# Download YOLOv5 weights
wget https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt

# Clone Adafruit_Python_PCA9685 repository for controlling the servo motor
git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
cd Adafruit_Python_PCA9685
sudo python3 setup.py install
cd ..

# Start the program with multithreading support
python3 main.py -t

