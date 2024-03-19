from google.cloud import texttospeech
import pygame
from io import BytesIO
from pdfminer.high_level import extract_pages
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

client = texttospeech.TextToSpeechClient.from_service_account_file("key.json")


# PDF dosyasının yolunu belirtin

# PDF dosyasının yolunu belirtin
pdf_path = "abi.pdf"

# Her bir sayfanın metnini çıkarmak için döngü
for page_layout in extract_pages(pdf_path):
    page_text = ""
    for element in page_layout:
        if hasattr(element, "get_text"):
            page_text += element.get_text()
    print(page_text.strip())  # Her sayfanın metnini yazdırın ve başındaki ve sonundaki boşlukları temizleyin
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=page_text.strip())

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

    print("\n---\n")  # Her sayfanın metni arasında bir ayracı ekleyin


