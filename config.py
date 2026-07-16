import os

# Vosk
VOSK_MODEL = "models/vosk-model-small-en-us-0.15"

SAMPLE_RATE = 16000
BLOCK_SIZE = 8000

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4.1-mini"

# ElevenLabs
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "")
