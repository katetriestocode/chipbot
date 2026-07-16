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

    for sentence in response.sentences:
        finalResponse += f"[{sentence.emotion}] {sentence.text} "
        tts.say(f"[{sentence.emotion}] {sentence.text}")

    print("BOT: " + finalResponse)

    tts.say(finalResponse)
