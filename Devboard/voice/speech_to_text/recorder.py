import pyaudio
import wave
import speech_recognition as sr
# import librosa


audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)
recognizer = sr.Recognizer()

# Listening in
# mic =sr.Microphone()

#Audio
frames = []

print('Start Recording: ')
count = 0 

try:
    while True:
        data = stream.read(1024)
        frames.append(data)
        # with open('audio_files.wav', 'wb') as f:
        #     file = f.write(b'{frames}')

        # sound_file = wave.open('audio_files.wav', 'wb')
        # sound_file.setnchannels(1)
        # sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        # sound_file.setframerate(44100)
        # sound_file.writeframes(b''.join(frames))
        output = wave.open('audio_files.wav','w')
        output.setparams((2,2,44100,0,'NONE','not compressed'))
        output.writeframes(data)
        output.close()

        # print(data)
        # break
        # res = sr.AudioData(data, sample_rate=44100, sample_width=1)
        res = sr.AudioFile('audio_files.wav')
        # print(res)
        print(count)
        count += 1
        with res as source:
            audio = recognizer.record(source)
        # Transcribe using Google API
        # print(mic)
        # with mic as source:
            
            # recognizer.adjust_for_ambient_noise(source)
            # audio = recognizer.listen(source)S
            # print(audio, 'audio')
        print("Translating your speech...")
        print(recognizer.recognize_google(audio_data=audio, language='en-US', show_all=True))
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    pass
