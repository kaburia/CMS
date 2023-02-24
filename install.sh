#!/bin/bash

# Update and upgrade the system
sudo apt-get update
# sudo apt-get -y upgrade


os=$(uname -a)

sudo pip install virtualenv 

if [[ $os == *"Kali"* ]]; then
  # Install Python 3.8 and set it to path
  echo "Kali Linux detected."
  sudo apt install python3.8 python3-pip
  sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
  
  python3.8 -m virtualenv CMS
#   virtualenv -p /usr/bin/python3.8 CMS
  
  # Install raspi-config
  sudo apt-get install -y raspi-config
  
  
  # Enable camera and GPIO pins using raspi-config
  sudo raspi-config nonint do_camera 0
  sudo raspi-config nonint do_spi 0
  sudo raspi-config nonint do_i2c 0
  sudo raspi-config nonint do_serial 0
  
elif [[ $os == *"raspbian"* ]]; then
  echo "Raspberry Pi OS detected."
  python3 -m virtualenv CMS
else
  echo "Unknown operating system."
fi

# Activate the virtual environment
source CMS/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up the coral USB accelerator
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update
sudo apt-get install -y libedgetpu1-std
sudo apt-get install python-pycoral

# Check the exit status of the command
if [ $? -eq 0 ]; then
    echo "Command ran successfully"
else
    echo "Command failed"
    python -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
fi

# Run the script
cd controls/

# Get the device's IP address
ip=$(hostname -I | awk '{print $1}')

# Replace the host parameter in the Python script with the IP address
sed -i "s/app.run(host=.*/app.run(host='${IP_ADDR}', debug=False, port=5500)/" controls.py

# Set a cronjob to start on boot with the ip address as host
# Write out current crontab to a file
crontab -l > mycron

# Echo new cron into cron file
echo "@reboot /usr/bin/python3 /controls.py" >> mycron

# Install new cron file
crontab mycron

# Remove the temporary file
rm mycron
