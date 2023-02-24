#!/bin/bash

# Update and upgrade the system
sudo apt-get update
# sudo apt-get -y upgrade


os=$(uname -a)


if [[ $os == *"kali-raspberry-pi"* ]]; then
  # Install Python 3.8 and set it to path building it from source
  echo "Kali Linux detected."
  sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
  wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
  tar -xf Python-3.8.0.tgz
  cd Python-3.8.0
  ./configure --enable-optimizations
  make -j 8
  sudo make altinstall
  
#   sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

  # Creating a virtual encironment
  cd ..
  sudo pip3.8 install virtualenv
  python3.8 -m virtualenv CMS
  
  # Activate the virtual environment
  source CMS/bin/activate
  pip install --upgrade pip
  
#   virtualenv -p /usr/bin/python3.8 CMS
    
  # Set up the coral USB accelerator
  echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo apt-get update
  sudo apt-get install -y libedgetpu1-std
  python -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
 
elif [[ $os == *"raspbian"* ]]; then
  echo "Raspberry Pi OS detected."
  
#   Creating a virtual environment
  sudo pip3 install virtualenv
  
  # Set up the coral USB accelerator
  echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo apt-get update
  sudo apt-get install -y libedgetpu1-std
  python3 -m virtualenv CMS
  sudo apt-get install python3-pycoral
else
  echo "Unknown operating system."
fi


# Install dependencies
pip install -r requirements.txt


# Run the script
cd controls/

# Get the device's IP address
ip=$(hostname -I | awk '{print $1}')

# Replace the host parameter in the Python script with the IP address
sed -i "s/app.run(host=.*/app.run(host='${ip}', debug=False, port=5500)/" controls.py

# Set a cronjob to start on boot with the ip address as host
# Write out current crontab to a file
sudo apt-get update
sudo apt-get install -y cron

# crontab -l > mycron

# Echo new cron into cron file
(crontab -l 2>/dev/null; echo "@reboot ../CMS/CMS/bin/python /controls.py") | crontab -

# Install new cron file
# crontab mycron

# Remove the temporary file
# rm mycron
