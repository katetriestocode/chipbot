from textSpeech.vosk_stt import VoskSTT
from LLM.openai_llm import OpenAILLM
from textSpeech.elevenlabs_tts import ElevenLabsTTS
import json

stt = VoskSTT()
llm = OpenAILLM()
tts = ElevenLabsTTS()

print("SnarkyShark is awake!")

while True:
    text = stt.listen()

    if not text:
        continue

    print(f"USER: {text}")

    response = llm.generate(text)

    data = json.loads(response)

    finalResponse = ""

    for sentence in data["sentences"]:
        emotion = sentence["emotion"]
        text = sentence["text"]

        finalResponse += f"[{emotion}] {text} "

    print("BOT: " + finalResponse)

    tts.say(finalResponse)
