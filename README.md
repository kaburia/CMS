# CMS

Control movement of the car based on either hand signals, voice input, text input or remotely controlled

![image](https://user-images.githubusercontent.com/88529649/211144449-fdc1ea0e-d5b2-4542-a7a4-0237eeda202b.png)

### Setting up Coral Dev Board 
https://docs.google.com/document/d/1kgKmQmAn292BDhxTejwZH-vQI1-5RpvkD-5UMVHZiNY/edit

## Installation Steps

### 1. Clone the repository and change directory into it
```
git clone https://github.com/kaburia/CMS.git
cd CMS
```

### 2. Create a Virtual Environment

```
pip install virtualenv
python3 -m venv CMS
```

 ### 3. Activate the Virtual Environment

 `Linux` 

 ```
source ./CMS/bin/activate
 ```
 `Windows`
 ``` 
 .\CMS\Scripts\activate
 ```

### 4. Install all Required Packages

```zsh
python -m pip install -r requirements.txt
```

### 5. Change directory to controls then run controls.py
```
cd controls
python controls.py
```
Open [http://localhost:5500](http://localhost:5500) with your browser to see the result.


