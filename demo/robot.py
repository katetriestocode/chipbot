import time

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation

import config
from audio import ChipBotAudioInterface

def main():
    if not config.ELEVENLABS_API_KEY or not config.ELEVENLABS_AGENT_ID:
        raise RuntimeError(
            "Set ELEVENLABS_API_KEY and ELEVENLABS_AGENT_ID in the environment."
        )

    client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
    conversation = Conversation(
        client=client,
        agent_id=config.ELEVENLABS_AGENT_ID,
        requires_auth=True,
        audio_interface=ChipBotAudioInterface(),
        callback_agent_response=lambda text: print(f"ChipBot: {text}"),
        callback_user_transcript=lambda text: print(f"User: {text}"),
    )

    print("ChipBot is awake. Ctrl+C to stop.")
    conversation.start_session()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nChipBot going to sleep.")
    finally:
        conversation.end_session()
        conversation_id = conversation.wait_for_session_end()
        print(f"Conversation ID: {conversation_id}")

if __name__ == "__main__":
    main()
