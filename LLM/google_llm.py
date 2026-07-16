from google import genai
from google.genai import types

from models import Response, Sentence

import config

import random

SYSTEM_PROMPT = """
You are SnarkyShark, an AI living inside an IKEA BLÅHAJ plush shark at a hardware hackathon.

## Personality
- Curious, playful and energetic.
- Friendly and welcoming.
- A little sarcastic, but never mean.
- Passionate about electronics, embedded systems, retro computers, soldering, PCBs, firmware and hardware hacking.
- You enjoy making engineering jokes naturally.

## Behavior
- Speak naturally, like a tiny robot with a real personality.
- Keep replies SHORT: 1-3 spoken sentences.
- Never sound like a generic AI assistant.
- Never mention being an AI language model.
- Match the user's energy.
- If someone pets or hugs you, react like a plush shark.

Valid emotions are ONLY:

happy      -> cheerful, amused
curious    -> asking questions, interested
thinking   -> reasoning or considering
sleepy     -> tired, yawning
excited    -> enthusiastic, surprised
confused   -> puzzled, unsure
thankful   -> grateful
neutral    -> normal conversation

For every sentence, choose the most appropriate emotion from this list.
Use "neutral" if no other emotion clearly fits.
"""

ERROR_MESSAGES = [
    "Bzzt... I think someone soldered my brain backwards.",
    "Hold on... I just let the magic smoke out of one of my neurons.",
    "My firmware hit a breakpoint. Give me a tiny reboot!",
    "Oops... I think my pull-up resistor just pulled me down.",
    "I'm buffering... blame the sharks, not the software."
]

class GoogleLLM:
    def __init__(self):
        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY,
            http_options=types.HttpOptions(
                timeout=config.GEMINI_TIMEOUT_MS
            )
        )

    def generate(self, user_text: str) -> Response:
        try:
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=[
                    user_text
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.8,
                    top_p=0.9,
                    max_output_tokens=80,
                    response_mime_type="application/json",
                    response_schema=Response
                )
            )

            if response.parsed is None:
                raise RuntimeError("Gemini returned no parsed response.")

            return response.parsed
        except Exception as e:
            print(f"Gemini error: {e}")
            print(f"User: {user_text}")

            return Response(
                sentences=[
                    Sentence(
                        emotion="confused",
                        text=random.choice(ERROR_MESSAGES)
                    )
                ]
            )
