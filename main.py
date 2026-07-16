from textSpeech.vosk_stt import VoskSTT
from LLM.openai_llm import OpenAILLM
from textSpeech.elevenlabs_tts import ElevenLabsTTS

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

    print(f"BOT: {response}")

    tts.say(response)
