#!/bin/bash

# Update and upgrade the system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python 3.8 and make it the default version
sudo apt-get install -y python3.8
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
sudo update-alternatives --set python /usr/bin/python3.8

# Install raspi-config
sudo apt-get install -y raspi-config

# Enable camera and GPIO pins using raspi-config
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0

# Install dependencies for ultrasonic sensor
sudo apt-get install -y python3-dev python3-rpi.gpio

# Install dependencies for servo motor control
sudo apt-get install -y pigpio

# Install dependencies for DC motor control
sudo apt-get install -y python3-pigpio

# Install PyCoral and EdgeTPU tools for Coral Dev Board
wget https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp38-cp38-linux_aarch64.whl
sudo apt-get install -y python3-pip
sudo python3 -m pip install numpy pillow opencv-python
sudo python3 -m pip install tflite_runtime-2.5.0-cp38-cp38-linux_aarch64.whl

# Download and convert YOLOv5s model for Coral Dev Board
wget https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt
python3 -m tflite_convert --output_file=yolov5s_edgetpu.tflite --saved_model_dir=yolov5s.pt --enable_v1_converter

# Enable pigpiod daemon at startup
sudo systemctl enable pigpiod.service

echo "Setup complete. Please reboot your Raspberry Pi."
