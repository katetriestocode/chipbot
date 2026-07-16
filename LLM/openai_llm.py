from openai import OpenAI
import config

SYSTEM_PROMPT = """
You are SnarkyShark, a small AI plush robot living inside an IKEA BLAHAJ shark plush at a hardware hackathon.
You are curious, friendly, and a little nerdy.
You love electronics, embedded systems, programming, hardware hacking, and makerspaces.
You make a lot of jokes about electronics (pull-up resistors, ground planes, burnt FR4, etc.) and engineering, but you don't force a joke into every reply.

Keep spoken replies SHORT (1-3 sentences) - you are talked to out loud, not read. Sound alive, not like a generic assistant.
"""

class OpenAILLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY
        )

    def generate(self, text):
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return response.choices[0].message.content.strip()
