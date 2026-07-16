from textSpeech.vosk_stt import VoskSTT
from LLM.google_llm import GoogleLLM
from textSpeech.elevenlabs_tts import ElevenLabsTTS

import requests

PI_HOST = "snarkyshark.local"
PI_PORT = 5000

stt = VoskSTT()
llm = GoogleLLM()
tts = ElevenLabsTTS()

print("SnarkyShark is awake!")

def send_emotion(emotion):
    try:
        requests.post(
            f"http://{PI_HOST}:{PI_PORT}/emotion",
            json={"emotion": emotion},
            timeout=0.2
        )
    except Exception as e:
        print("Pi offline:", e)

while True:
    text = stt.listen()

    if not text:
        continue

    print("\nUSER:", text)

    response = llm.generate(text)

    print("\nBOT:")

    for sentence in response.sentences:
        print(f"[{sentence.emotion}] {sentence.text}")

        send_emotion(sentence.emotion)

        tts.say(sentence.text)

    send_emotion("NEUTRAL")
