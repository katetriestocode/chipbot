import speech_recognition as sr

recognizer = sr.Recognizer()

def speech_to_text():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,              # wait max 5 s to listen
                phrase_time_limit=10    # register max 10 s
            )

            text = recognizer.recognize_google(audio)

            return text.lower()
        except sr.WaitTimeoutError: # No speech detected
            return None
        except sr.UnknownValueError: # Audio ununderstandable
            return None
        except sr.RequestError as e:
            return None
