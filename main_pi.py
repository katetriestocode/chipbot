from textSpeech.elevenlabs_tts import ElevenLabsTTS
from servoMotors import ServoMotors

import serial

tts = ElevenLabsTTS()

ser = serial.Serial("/dev/ttyACM0", 115200)

servos = ServoMotors()

print("SnarkyShark Pi is ready!")

try:
    while True:
        line = ser.readline().decode().strip()

        if not line:
            continue

        print(line)

        try:
            command, emotion, text = line.split("|",2)
        except ValueError:
            continue

        if command != "SAY":
            continue

        print(emotion, text)

        servos.react()
        servos.set_emotion(emotion)

        try:
            tts.say(text)
        except Exception as e:
            print("TTS error:", e)

        servos.set_emotion("NEUTRAL")
finally:
    servos.stop()
