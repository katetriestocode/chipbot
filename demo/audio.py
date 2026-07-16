import queue
import threading
import time

import sounddevice as sd
from elevenlabs.conversational_ai.conversation import AudioInterface

import demo.config as config


class ChipBotAudioInterface(AudioInterface):
    def __init__(self):
        self._input_stream = None
        self._output_stream = None
        self._output_queue: "queue.Queue[bytes]" = queue.Queue()
        self._output_thread = None
        self._should_stop = threading.Event()

    def start(self, input_callback):
        self._should_stop.clear()

        def _on_mic_chunk(indata, frames, time_info, status):
            if status:
                print(f"[audio] input status: {status}")
            input_callback(bytes(indata))

        self._input_stream = sd.RawInputStream(
            samplerate=config.AUDIO_SAMPLE_RATE,
            channels=config.AUDIO_CHANNELS,
            dtype="int16",
            blocksize=config.AUDIO_CHUNK_SAMPLES,
            device=config.AUDIO_INPUT_DEVICE,
            callback=_on_mic_chunk,
        )
        self._input_stream.start()

        self._output_stream = sd.RawOutputStream(
            samplerate=config.AUDIO_SAMPLE_RATE,
            channels=config.AUDIO_CHANNELS,
            dtype="int16",
            device=config.AUDIO_OUTPUT_DEVICE,
        )
        self._output_stream.start()

        self._output_thread = threading.Thread(target=self._output_loop, daemon=True)
        self._output_thread.start()

    def stop(self):
        self._should_stop.set()
        if self._output_thread:
            self._output_thread.join(timeout=2)
        if self._input_stream:
            self._input_stream.stop()
            self._input_stream.close()
        if self._output_stream:
            self._output_stream.stop()
            self._output_stream.close()

    def output(self, audio: bytes):
        self._output_queue.put(audio)

    def interrupt(self):
        while not self._output_queue.empty():
            try:
                self._output_queue.get_nowait()
            except queue.Empty:
                break

    def _output_loop(self):
        while not self._should_stop.is_set():
            try:
                chunk = self._output_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            if self._output_stream:
                self._output_stream.write(chunk)

if __name__ == "__main__":
    audio = ChipBotAudioInterface()
    audio.start(lambda chunk: audio.output(chunk))

    time.sleep(5)

    audio.stop()
