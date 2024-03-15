from google.cloud import texttospeech
import pygame
from io import BytesIO

client = texttospeech.TextToSpeechClient.from_service_account_file("key.json")

Text = input()
# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=Text)

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
# voice parameters and audio file type
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
