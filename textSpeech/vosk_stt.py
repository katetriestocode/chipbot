import json
import queue

import sounddevice as sd
from vosk import Model, KaldiRecognizer

import config

class VoskSTT:
    def __init__(self):
        self.model = Model(config.VOSK_MODEL)
        self.recognizer = KaldiRecognizer(
            self.model,
            config.SAMPLE_RATE
        )

        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)

        self.q.put(bytes(indata))

    def listen(self):
        print("Listening...")

        with sd.RawInputStream(
            samplerate=config.SAMPLE_RATE,
            blocksize=config.BLOCK_SIZE,
            dtype='int16',
            channels=1,
            callback=self.callback
        ):

            while True:
                data = self.q.get()

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(
                        self.recognizer.Result()
                    )

                    text = result.get("text", "").strip()

                    if text:
                        return text
