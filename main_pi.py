from textSpeech.elevenlabs_tts import ElevenLabsTTS

import serial

tts = ElevenLabsTTS()

ser = serial.Serial("/dev/ttyACM0", 115200)

print("SnarkyShark Pi is ready!")

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

    # start_servos(emotion)

    tts.say(text)

    # stop_servos()
