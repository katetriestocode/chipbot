# This is to run all the AI locally

from textSpeech.vosk_stt import VoskSTT
from LLM.google_llm import GoogleLLM
from textSpeech.elevenlabs_tts import ElevenLabsTTS

stt = VoskSTT()
llm = GoogleLLM()
tts = ElevenLabsTTS()

print("SnarkyShark is awake!")

while True:
    text = stt.listen()

    if not text:
        continue

    print(f"USER: {text}")

    response = llm.generate(text)

    finalResponse = ""

    print("BOT: ")

    for sentence in response.sentences:
        print(f"   [{sentence.emotion}] {sentence.text} ")
        finalResponse += f"{sentence.text} "

    tts.say(finalResponse)
