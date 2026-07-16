from elevenlabs.client import ElevenLabs
from elevenlabs import play

import config

class ElevenLabsTTS:
    def __init__(self):
        self.client = ElevenLabs(
            api_key=config.ELEVEN_API_KEY
        )

    def say(self, text):
        audio = self.client.text_to_speech.convert(
            voice_id=config.ELEVEN_VOICE_ID,
            text=text,
            model_id="eleven_flash_v2_5"
        )

        play(audio)
