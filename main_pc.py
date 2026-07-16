from textSpeech.vosk_stt import VoskSTT
from LLM.google_llm import GoogleLLM

import socket

PI_IP = "172.20.10.5"
PORT = 5000

def send_pi(emotion, text):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((PI_IP, PORT))

        s.sendall(
            f"SAY|{emotion}|{text}".encode()
        )

        s.close()

    except Exception as e:
        print("Pi offline:", e)

stt = VoskSTT()
llm = GoogleLLM()

print("SnarkyShark is awake!")

while True:
    text = stt.listen()

    if not text:
        continue

    print("\nUSER:", text)

    response = llm.generate(text)

    print("\nBOT:")

    for sentence in response.sentences:
        print(sentence.emotion, sentence.text)

        send_pi(
            sentence.emotion,
            sentence.text
        )
