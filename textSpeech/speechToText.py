import speech_recognition as sr
import demo.config as config

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._vosk_model = None
 
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
 
    def listen_once(self, timeout: float = 5.0, phrase_time_limit: float = 8.0) -> str:
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                return ""
 
        if config.STT_BACKEND == "google":
            return self._transcribe_google(audio)
        elif config.STT_BACKEND == "vosk":
            return self._transcribe_vosk(audio)
        else:
            raise ValueError(f"Unknown STT_BACKEND: {config.STT_BACKEND}")
 
    def _transcribe_google(self, audio) -> str:
        try:
            return self.recognizer.recognize_google(audio, language=config.STT_LANGUAGE)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            print(f"[speech] Google STT request failed: {exc}")
            return ""
 
    def _transcribe_vosk(self, audio) -> str:
        # Lazy import + lazy model load: keeps startup fast if you're using
        # the google backend, and avoids loading the model twice.
        if self._vosk_model is None:
            import vosk
 
            self._vosk_model = vosk.KaldiRecognizer(
                vosk.Model(config.VOSK_MODEL_PATH), 16000
            )
 
        raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
        if self._vosk_model.AcceptWaveform(raw_data):
            import json
 
            result = json.loads(self._vosk_model.Result())
            return result.get("text", "")
        return ""
 
 
if __name__ == "__main__":
    stt = SpeechToText()
    print("Listening... say something.")
    heard = stt.listen_once()
    print(f"Heard: {heard!r}")
 