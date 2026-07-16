from textSpeech.vosk_stt import VoskSTT
from LLM.google_llm import GoogleLLM
import serial
import time
import config

BAUD = 115200

stt = VoskSTT()
llm = GoogleLLM()

ser = serial.Serial(SERIAL_PORT, BAUD)
time.sleep(2)

print("SnarkyShark PC is ready!")

while True:
    text = stt.listen()

    if not text:
        continue

    print(f"USER: {text}")

    response = llm.generate(text)

    for sentence in response.sentences:
        command = f"SAY|{sentence.emotion}|{sentence.text}\n"

        print("SEND:", command.strip())

        ser.write(command.encode("utf-8"))
