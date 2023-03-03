#!/bin/bash

# Update and upgrade the system
sudo apt-get update
sudo apt-get -y upgrade


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
pip install rpi.gpio


# Run the script
cd controls/

# Get router IP address
router_ip=$(ip route | grep default | awk '{print $3}')

# Get router DNS server
router_dns=$(nmcli dev show | grep 'IP4.DNS' | awk '{print $2}')

# Set a static IP address
sudo sed -i '$a\interface eth0' /etc/dhcpcd.conf
sudo sed -i '$a\static ip_address='"${router_ip}"'157/24' /etc/dhcpcd.conf
sudo sed -i '$a\static routers='"${router_ip}" /etc/dhcpcd.conf
sudo sed -i '$a\static domain_name_servers='"${router_dns}" /etc/dhcpcd.conf

# Get the device's IP address
ip=$(hostname -I | awk '{print $1}')

# Enable port forwarding for port 5500
sudo iptables -t nat -A PREROUTING -p tcp --dport 5500 -j DNAT --to-destination "${ip}:80"
sudo iptables -t nat -A POSTROUTING -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
# Make port forwarding rules persistent across reboots
sudo sed -i '$a\iptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local

# Replace the host parameter in the Python script with the IP address
sed -i "s/app.run(host=.*/app.run(host='${ip}', debug=False, port=5500)/" controls.py


# Restart the OpenVPN service

# TODO set up a crontab job on reboot to setup the ip address as host and set up openvpn and port forwarding as a separate bash script

# # Set a cronjob to start on boot with the ip address as host
# # Write out current crontab to a file
# sudo apt-get update
# sudo apt-get install -y cron

# # crontab -l > mycron
# # Changing to root
# sudo su
# cd .. 
# source CMS/bin/activate
# cd controls/

# if [[ $os == *"kali-raspberry-pi"* ]]; then
#   # Echo new cron into cron file
#   (crontab -l 2>/dev/null; echo "@reboot /home/kali/CMS/CMS/bin/python /home/kali/CMS/controls/controls.py") | crontab -
# else
#   echo "This script is only compatible with Kali Linux Raspberry Pi OS."
# fi

# # Check if user is root
# if [ "$EUID" -ne 0 ]
#   then echo "Please run as root"
# fi

# # Add root privileges to run crontab
# sudo chmod u+s /usr/bin/crontab
# sudo chmod g+s /usr/bin/crontab
# sudo chown root:crontab /usr/bin/crontab
# sudo chown root:crontab /var/spool/cron/crontabs
# sudo chmod 1730 /var/spool/cron/crontabs

# echo "Root privileges added to run crontab successfully!"



python controls.py

