import wave
import pyaudio
# import whisper
import time
import speech_recognition as sr

# Loading the whisper model
# model = whisper.load_model("base")

# Instaniate recognizer class
recognizer = sr.Recognizer()

def RecordInit(sampling_rate=44100):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)
    return audio, stream

# Record Audio
def record_audio(audiofile):
    print('Start Recording: ')
    frames = []
    audio, stream = RecordInit()
    start = time.time()
    try:
    
        while True:
            data = stream.read(1024)
            frames.append(data)
            sound_file = wave.open(audiofile, 'wb')
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))
            end = time.time()
            diff = int(end - start)
            if diff == 5:
                break

    except KeyboardInterrupt:
        print('System Interrupted!!')

# # Transcribe
# def transcribe(audiofile):
#     print('Transcribing....')
#     result = model.transcribe(audiofile)
#     return result['text']


def transcribe(audio_file):
    res = sr.AudioFile(audio_file)
    with res as source:
        audio = recognizer.record(source)
    # Transcribe speech using Google web API
    return recognizer.recognize_google(audio_data=audio, language='en-US')
    

if __name__ == '__main__':
    record_audio('audio_files.wav')
    print(transcribe('audio_files.wav'))