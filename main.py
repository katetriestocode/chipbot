import * from "textSpeech/speechToText.py"
import * from "textSpeech/textToSpeech.py"
from demo.agent import ChipBot

while True:
    """ text = speech_to_text()

    if text is not None:
        textToSpeech(text) """
    bot = ChipBot()
    bot.start()
