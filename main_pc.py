from textSpeech.vosk_stt import VoskSTT
from LLM.google_llm import GoogleLLM
from textSpeech.elevenlabs_tts import ElevenLabsTTS

import socket

PI_HOST = "snarkyshark.local"
PI_PORT = 5000

stt = VoskSTT()
llm = GoogleLLM()
tts = ElevenLabsTTS()

print("SnarkyShark is awake!")

def send_pi(emotion, text):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((PI_HOST, PI_PORT))

        sock.sendall(f"SAY|{emotion}|{text}".encode())

        sock.close()
    except Exception as e:
        print("Pi offline:", e)

while True:
    text = stt.listen()

    if not text:
        continue

    print(f"\nUSER: {text}")

    response = llm.generate(text)

    print("\nBOT:")

    for sentence in response.sentences:
        print(f"[{sentence.emotion}] {sentence.text}")

        send_pi(sentence.emotion, sentence.text)

        tts.say(sentence.text)

    send_pi("NEUTRAL", "")
