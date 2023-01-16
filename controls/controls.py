from flask import Flask, redirect, url_for, render_template, request, Response
import sys

camera_path = r'C:\Users\Austin\Desktop\Agent\Car movements\CMS\Devboard\camera'
# # voice = r'C:\Users\Austin\Desktop\Agent\Car movements\CMS\Devboard\voice\speech_to_text'

sys.path.insert(0, f'{camera_path}')
from pycoral import camera_inference # Testing the images seen
from camera_input import camera_input #Turning on the camera
# # # Image input
# # from object_detection import detector

# sys.path.insert(0, f'{voice}')
# from recorder import record_audio, transcribe # Recording and transcribing


# Phone number stored as a session for less than a day

app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/camera')
def video():
    return Response(camera_inference(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/voice')
def voice():
    return render_template("index.html")

@app.route('/image')
def image():
    return render_template("index.html")

@app.route('/text')
def text():
    return render_template("index.html")




# Passing parameters
# @app.route('/name')
# def user():
#     return render_template("home.html")



# # Redirecting from admin
# @app.route('/admin')
# def admin():
#     return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)

#intents file
'''
From the text input, output the possible commands
to send through the I2C to the arduino for processing the data can also 
be sent to the LCD Display
'''