#!/bin/bash


# Get the device's IP address and store it in the "ip" variable
ip=$(hostname -I | awk '{print $1}')

# Replace the host parameter in the Flask app.run function with the "ip" variable
sed -i "s/app.run(host='[^']*'/app.run(host='${ip}'/" /home/pi/Desktop/CMS/controls/controls.py

# Start the Flask application
python3 /home/pi/Desktop/CMS/controls/controls.py

# Start up the fan
cd /home/pi/RGB_Cooling_HAT/
sudo sh install.sh