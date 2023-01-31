from flask import Flask, flash, request, redirect, url_for, render_template, Response, send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField


import sys, os
# from werkzeug.utils import secure_filename

camera_path = '../Devboard/camera'
# # voice = r'C:\Users\Austin\Desktop\Agent\Car movements\CMS\Devboard\voice\speech_to_text'

sys.path.insert(0, f'{camera_path}')
# from pycoral_t import camera_inference # Testing the images seen
# from camera_input import camera_input #Turning on the camera
from detector import model_detection
# # # Image input
# # from object_detection import detector

# sys.path.insert(0, f'{voice}')
# from recorder import record_audio, transcribe # Recording and transcribing


# Phone number stored as a session for less than a day

app = Flask(__name__)

UPLOAD_FOLDER = '../controls/static/images'

app.secret_key = "secret key"
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Saving with images extensions
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
# patch_request_class(app)  # set maximum file size, default is 16MB

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route(f'/{UPLOAD_FOLDER}/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename )

@app.route('/')
def index():
    return render_template("index.html")

# Image input page
@app.route('/image', methods=['GET', 'POST'])
def image():    
    form = UploadForm()
    # True without errors
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        
    else:
        file_url = None
    if request.method == 'POST':
        return redirect(url_for('model_detect'))
    return render_template('image.html', form=form, file_url=file_url)

@app.route('/camera', methods=['GET', 'POST'])
def cam():
    return render_template('camera.html')

# Signals inference
@app.route('/cam')
def video():
    return Response(camera_inference(),mimetype='multipart/x-mixed-replace; boundary=frame')


# Model detection path
@app.route('/detect')
def model():
    return Response(model_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detector')
def model_detect():
    flash('Detection page....')
    return render_template('detector.html')
    


'''
TEST THIS
IF REDIRECTED FROM A URL USE DISPLAY ONLY THE CAMERA
IF 
'''

# What the camera sees
@app.route('/camInput')
def camInput():
    return Response(camera_inference(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/voice')
def voice():
    return render_template("voice.html")

@app.route('/basetest')
def test():
    return render_template('base.html')


'''
Using stable Diffusion to convert text to images
'''
@app.route('/text')
def text():
    return render_template("text.html")

@app.route('/about')
def about():
    return render_template("about.html")


 



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

