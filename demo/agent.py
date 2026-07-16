from elevenlabs.client import ElevenLabs
import demo.config as config

class ChipBot:

    def __init__(self):
        self.client = ElevenLabs(
            api_key=config.ELEVENLABS_AGENT_ID
        )

    def start(self):
        conversation = self.client.conversational_ai.start_session(
            agent_id=config.ELEVENLABS_AGENT_ID,

            on_user_transcript=self.user_transcript,

            on_agent_response=self.agent_response,

            on_state_change=self.state_changed
        )

        conversation.run()

    def user_transcript(self, text):
        print(f"USER: {text}")

    def agent_response(self, text):
        print(f"BOT: {text}")

    def state_changed(self, state):
        print(state)
