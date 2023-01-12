import wave
import pyaudio
import whisper

# Loading the whisper model
model = whisper.load_model("base")

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
    try:

        while True:
            data = stream.read(1024)
            frames.append(data)
            sound_file = wave.open(audiofile, 'wb')
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))

    except KeyboardInterrupt:
        print('System Interrupted!!')

# Transcribe
def transcribe(audiofile):
    print('Transcribing....')
    result = model.transcribe(audiofile)
    return result['text']

if __name__ == '__main__':
    record_audio('audio_files.wav')
    print(transcribe('audio_files.wav'))