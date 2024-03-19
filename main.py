import pyaudio
from google.cloud import texttospeech,speech
import pygame
from io import BytesIO
from pdfminer.high_level import extract_pages
import firebase_admin
from firebase_admin import credentials,storage
import openai
import wave
import json
def record_audio(filename, duration=5, rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()

    # Ses kaydı için özellikler
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    # Ses verisini kaydet
    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Ses akışını kapat
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Ses verisini WAV dosyasına yaz
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    return filename

# Kaydedilecek ses dosyasının adı
filename = "recorded_audio.wav"
duration = 5

# Ses kaydını başlat
recorded_file = record_audio(filename, duration)

client_speech=speech.SpeechClient.from_service_account_file("key.json")
with open(filename,"rb") as f:
    wav_data = f.read()

audio_file=speech.RecognitionAudio(content = wav_data)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz =44100,
    language_code="en-US"
)

response = client_speech.recognize(
    config=config,
    audio=audio_file
)
transcript = response.results[0].alternatives[0].transcript
print(transcript)
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",  # Kullanmak istediğiniz GPT-3 modeli
        messages=[{"role": "system", "content": prompt}],
        max_tokens=50  # Oluşturulacak metnin maksimum uzunluğu
    )
    return response.choices[0].message['content'].strip()




openai.api_key = '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'


user_input = transcript

generated_text = generate_text(user_input)

print("ChatGPT: ", generated_text)

client = texttospeech.TextToSpeechClient.from_service_account_file("key.json")


# PDF dosyasının yolunu belirtin

synthesis_input = texttospeech.SynthesisInput(text=generated_text)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", name="en-US-Studio-O"
    )
    # Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16  # WAV formatı
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio fi
    # le type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
audio_bytes = BytesIO(response.audio_content)

    # Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load(audio_bytes)
pygame.mixer.music.play()

    # Keep the program running until the audio finishes playing
while pygame.mixer.music.get_busy():
    continue
