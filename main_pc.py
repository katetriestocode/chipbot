from textSpeech.vosk_stt import VoskSTT
from LLM.google_llm import GoogleLLM
from textSpeech.elevenlabs_tts import ElevenLabsTTS

import serial

import config

BAUD = 115200

try:
    ser = serial.Serial(
        config.SERIAL_PORT,
        BAUD,
        timeout=0.1
    )
    print(f"Pi connected on {config.SERIAL_PORT}")
except Exception as e:
    ser = None
    print(f"Running without Pi ({e})")


def send_pi(command: str):
    if ser is None:
        return

    try:
        ser.write((command + "\n").encode())
    except Exception as e:
        print("Serial error:", e)

stt = VoskSTT()
llm = GoogleLLM()
tts = ElevenLabsTTS()

print("SnarkyShark is awake!")

while True:
    text = stt.listen()

    if not text:
        continue

    print(f"\nUSER: {text}")

    response = llm.generate(text)

    print("\nBOT:")

    for sentence in response.sentences:
        print(f"[{sentence.emotion}] {sentence.text}")

        send_pi(sentence.emotion.upper())

        tts.say(sentence.text)
