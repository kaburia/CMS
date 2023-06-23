# CMS

<!--Control movement of the car based on either hand signals, voice input, text input or remotely controlled  -->
<!-- [image](https://user-images.githubusercontent.com/88529649/211144449-fdc1ea0e-d5b2-4542-a7a4-0237eeda202b.png) -->
<!--![image](https://user-images.githubusercontent.com/88529649/227775070-3eb1a834-d7ed-4acf-bfbc-1aae2de536d4.png)  -->


## Introduction
CMS is a project that aims to create a self-driving remote-controlled car that can track objects and navigate around obstacles in real-time. The system uses a combination of hardware components, such as a Raspberry Pi 4 Model B and a Coral USB Accelerator, and software algorithms, including YOLOv5, Deep SORT, A*, SLAM, and reinforcement learning.

## Objectives
The objectives of the Autonomous RC Car System are as follows:

* Develop a robust system for object tracking and path planning using a Raspberry Pi and a Coral USB Accelerator.
* Implement state-of-the-art software algorithms, including YOLOv5 for object detection, Deep SORT for object tracking, A* and SLAM for path planning, and reinforcement learning for optimization.
* Integrate the software and hardware components to create a functioning autonomous RC car system.
* Test and validate the system in various real-world scenarios, including indoor and outdoor environments, and refine the system based on feedback and performance metrics.

## Methods
### Hardware
The Autonomous RC Car System uses the following hardware components:

* Raspberry Pi 4 Model B
* Coral USB Accelerator
* Ultrasonic sensor
* Servo motor
* Infrared sensors
* Camera
* DC Motors

The hardware components are assembled onto a PCB used as a shield connected to the Raspberry Pi, with a power bank for energy supply.

### Software
The system uses the Robot Operating System (ROS) as the underlying framework for the software development and is programmed using Python. The software incorporates the following algorithms:

* YOLOv5 for object detection
* Deep SORT for object tracking
* A* and SLAM for path planning
* Reinforcement learning for optimization

## Integration
The software and hardware components are integrated using ROS nodes and topics, with the Coral USB Accelerator handling the object detection and tracking algorithms.

## Testing
The system is tested in various scenarios to evaluate its performance, including indoor and outdoor environments with varying light conditions, different types of obstacles, and varying speeds of the target object.

## Expected Outcomes
The expected outcomes of the Autonomous RC Car System project are:

* A functioning autonomous RC car system that can track objects and navigate around obstacles in real-time
* Improved algorithms for object detection, tracking, and path planning that can be used in other applications
* Increased understanding of the challenges and limitations of autonomous systems and potential areas for further development
* Potential for commercial applications in search and rescue, surveillance, and logistics


## Installation

### First time boot up of device
```
git clone https://github.com/kaburia/CMS.git
cd CMS
chmod +x install.sh
./install.sh
```
### Setting up Coral Dev Board 
``Windows``

https://docs.google.com/document/d/1kgKmQmAn292BDhxTejwZH-vQI1-5RpvkD-5UMVHZiNY/edit

## Contributions
Contributions to the Autonomous RC Car System project are welcome. Please submit a pull request with your changes or open an issue for any bugs or feature requests.
