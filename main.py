import * from "textSpeech/speechToText.py"
import * from "textSpeech/textToSpeech.py"

while True:
    text = speech_to_text()

    if text is not None:
        textToSpeech(text)
