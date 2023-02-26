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

# Get the device's IP address
ip=$(hostname -I | awk '{print $1}')

# Replace the host parameter in the Python script with the IP address
sed -i "s/app.run(host=.*/app.run(host='${ip}', debug=False, port=5500)/" controls.py

# Install OpenVPN
sudo apt-get update
sudo apt-get install openvpn easy-rsa -y

# Create the OpenVPN server configuration file
sudo cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/
sudo gzip -d /etc/openvpn/server.conf.gz
sudo sed -i 's/;user nobody/user nobody/' /etc/openvpn/server.conf
sudo sed -i 's/;group nogroup/group nogroup/' /etc/openvpn/server.conf
sudo sed -i 's/;push "redirect-gateway def1 bypass-dhcp"/push "redirect-gateway def1 bypass-dhcp"/' /etc/openvpn/server.conf
sudo sed -i 's/;push "dhcp-option DNS 208.67.222.222"/push "dhcp-option DNS 8.8.8.8"/' /etc/openvpn/server.conf
sudo sed -i 's/;user nobody/user nobody/' /etc/openvpn/server.conf
sudo sed -i 's/;group nogroup/group nogroup/' /etc/openvpn/server.conf

# Generate the Diffie-Hellman parameters
sudo openssl dhparam -out /etc/openvpn/dh.pem 2048

# Generate the server certificate and key
sudo easyrsa init-pki
sudo easyrsa build-ca
sudo easyrsa gen-req server nopass
sudo easyrsa sign-req server server

# Generate client certificates and keys
sudo easyrsa gen-req client1 nopass
sudo easyrsa sign-req client client1

# Create the OpenVPN client configuration files
sudo mkdir -p /etc/openvpn/client-configs/files
sudo cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf /etc/openvpn/client-configs/base.conf
sudo sed -i 's/remote my-server-1 1194/remote YOUR_SERVER_IP_ADDRESS YOUR_PORT/' /etc/openvpn/client-configs/base.conf
sudo sed -i 's/;user nobody/user nobody/' /etc/openvpn/client-configs/base.conf
sudo sed -i 's/;group nogroup/group nogroup/' /etc/openvpn/client-configs/base.conf
sudo sed -i 's/ca ca.crt/#ca ca.crt/' /etc/openvpn/client-configs/base.conf
sudo sed -i 's/cert client.crt/#cert client.crt/' /etc/openvpn/client-configs/base.conf
sudo sed -i 's/key client.key/#key client.key/' /etc/openvpn/client-configs/base.conf
echo "<ca>" | sudo tee -a /etc/openvpn/client-configs/base.conf
sudo cat /etc/openvpn/pki/ca.crt | sudo tee -a /etc/openvpn/client-configs/base.conf
echo "</ca>" | sudo tee -a /etc/openvpn/client-configs/base.conf
sudo cp /etc/openvpn/pki/issued/client1.crt /etc/openvpn/client-configs/files/
sudo cp /etc/openvpn/pki/private/client1.key /etc/openvpn/client-configs/files/

# Set up port forwarding on the router
sudo ufw allow 1194/udp
sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p
sudo iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

# Restart the OpenVPN service

# TODO set up a crontab job on reboot to setup the ip address as host and set up openvpn and port forwarding as a separate bash script

# Set a cronjob to start on boot with the ip address as host
# Write out current crontab to a file
sudo apt-get update
sudo apt-get install -y cron

# crontab -l > mycron
# Changing to root
sudo su
cd .. 
source CMS/bin/activate
cd controls/

if [[ $os == *"kali-raspberry-pi"* ]]; then
  # Echo new cron into cron file
  (crontab -l 2>/dev/null; echo "@reboot /home/kali/CMS/CMS/bin/python /home/kali/CMS/controls/controls.py") | crontab -
else
  echo "This script is only compatible with Kali Linux Raspberry Pi OS."
fi

# Check if user is root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
fi

# Add root privileges to run crontab
sudo chmod u+s /usr/bin/crontab
sudo chmod g+s /usr/bin/crontab
sudo chown root:crontab /usr/bin/crontab
sudo chown root:crontab /var/spool/cron/crontabs
sudo chmod 1730 /var/spool/cron/crontabs

echo "Root privileges added to run crontab successfully!"



python controls.py

