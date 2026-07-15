import pyttsx3

def textToSpeech(text):
    engine = pyttsx3.init()

    engine.say(text)
    engine.runAndWait()
