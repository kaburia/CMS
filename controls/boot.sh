# Get the device's IP address
ip=$(hostname -I | awk '{print $1}')
sed -i "s/app.run(host=.*/app.run(host='${ip}', debug=False, port=5500)/" /home/pi/Desktop/CMS/controls/controls.py

# Start up the fan
cd /home/pi/RGB_Cooling_HAT/
sudo sh install.sh

# Move back to execute
cd /home/pi/Desktop/CMS/controls
python controls.py
