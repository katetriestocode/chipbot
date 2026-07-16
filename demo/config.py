import os

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_AGENT_ID = os.environ.get("ELEVENLABS_AGENT_ID", "")

#   GPIO18 (pin 12) = BCLK   -> shared by mic and amp
#   GPIO19 (pin 35) = LRCLK  -> shared by mic and amp
#   GPIO20 (pin 38) = DIN    -> from mic's data-out pin (e.g. INMP441 "SD")
#   GPIO21 (pin 40) = DOUT   -> to amp's data-in pin   (e.g. MAX98357A "DIN")
AUDIO_SAMPLE_RATE = 16000  # required by the ElevenLabs Agent audio protocol
AUDIO_CHANNELS = 1
AUDIO_CHUNK_SAMPLES = 1600  # 100ms chunks at 16kHz

AUDIO_INPUT_DEVICE = os.environ.get("CHIPBOT_AUDIO_INPUT_DEVICE", "plughw:1,0")
AUDIO_OUTPUT_DEVICE = os.environ.get("CHIPBOT_AUDIO_OUTPUT_DEVICE", "plughw:1,0")
