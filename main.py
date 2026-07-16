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

    print("USER: " + text)

    response = llm.generate(text)

    print("BOT: " + response)

    tts.say(response)
