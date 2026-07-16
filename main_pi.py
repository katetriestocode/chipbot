from textSpeech.elevenlabs_tts import ElevenLabsTTS
from servoMotors import ServoMotors

import socket

HOST = "0.0.0.0"
PORT = 5000

tts = ElevenLabsTTS()
servos = ServoMotors()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("SnarkyShark Pi ready on port", PORT)

try:
    while True:
        conn, addr = server.accept()

        data = conn.recv(8192).decode().strip()
        conn.close()

        if not data:
            continue

        print(data)

        try:
            command, emotion, text = data.split("|", 2)
        except ValueError:
            continue

        if command != "SAY":
            continue

        servos.react()
        servos.set_emotion(emotion)

        try:
            tts.say(text)
        except Exception as e:
            print(e)

        servos.set_emotion("NEUTRAL")
finally:
    servos.stop()
