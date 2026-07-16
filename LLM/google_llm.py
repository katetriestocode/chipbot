from google import genai
from google.genai import types

from LLM.models import Response, Sentence

import config
import json
import random
import time

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

Return ONLY valid JSON.

Example:

{
  "sentences": [
    {
      "emotion": "happy",
      "text": "Hello!"
    }
  ]
}

Valid emotions:

happy
curious
thinking
sleepy
excited
confused
thankful
neutral

Output ONLY the JSON object.
"""

ERRORS = [
    "Bzzt... I think someone soldered my brain backwards.",
    "Oops... my RAM just escaped through a GPIO pin.",
    "Hold on... I dropped a few electrons.",
    "My firmware just took an unexpected coffee break.",
    "I think someone connected VCC to my brain."
]

class GoogleLLM:
    def __init__(self):
        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY,
            http_options=types.HttpOptions(
                timeout=config.GEMINI_TIMEOUT_MS
            )
        )

    def generate(self, user_text) -> Response:
        try:
            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=config.GEMINI_MODEL,
                        contents=user_text,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.8,
                            top_p=0.9,
                            max_output_tokens=300,
                            thinking_config=types.ThinkingConfig(
                                thinking_budget=0
                            ),
                            response_mime_type="application/json",
                        )
                    )

                    print("\n===== GEMINI RAW TEXT =====")
                    print(response.text)

                    data = json.loads(response.text)

                    return Response.model_validate(data)
                except Exception as e:
                    print(f"Gemini attempt {attempt+1}/3 failed: {e}")

                    if attempt < 2:
                        time.sleep(1)
                    else:
                        raise
        except Exception as e:
            print("\n===== GEMINI ERROR =====")
            print(e)
            print("User:", user_text)

            try:
                print("\n===== FULL RESPONSE =====")
                from pprint import pprint
                pprint(response.to_json_dict())
            except Exception:
                pass

            return Response(
                sentences=[
                    Sentence(
                        emotion="confused",
                        text=random.choice(ERRORS)
                    )
                ]
            )
