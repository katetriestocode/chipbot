from pydantic import BaseModel
from typing import Literal

class Sentence(BaseModel):
    emotion: Literal[
        "happy",
        "curious",
        "thinking",
        "sleepy",
        "excited",
        "confused",
        "thankful",
        "neutral",
    ]
    text: str

class Response(BaseModel):
    sentences: list[Sentence]
