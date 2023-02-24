# CMS

Control movement of the car based on either hand signals, voice input, text input or remotely controlled

![image](https://user-images.githubusercontent.com/88529649/211144449-fdc1ea0e-d5b2-4542-a7a4-0237eeda202b.png)

### Setting up Coral Dev Board 
``Windows``
https://docs.google.com/document/d/1kgKmQmAn292BDhxTejwZH-vQI1-5RpvkD-5UMVHZiNY/edit

## Installation

### First time boot up of device
```
git clone https://github.com/kaburia/CMS.git
cd CMS
chmod +x install.sh
./install.sh
ip addr show | grep -w inet | awk '{print $2}' | awk -F / '{print $1}'
```




