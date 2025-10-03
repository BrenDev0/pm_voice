from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import os

class DeepGramService:
    @staticmethod
    def on_open(open_event=None):
            print("Deepgram connection open")

    @staticmethod
    def on_error(error):
        print(f"Deepgram error: {error}")

    @staticmethod
    def on_close(close_event=None):
        print("Deepgram connection closed")

    @staticmethod
    def get_options(
        model: str,
        language: str
    ):
        options = LiveOptions(
            model=model,
            language=language,
            smart_format=True,
            interim_results=False
        )
         
        return options
         
    @staticmethod
    def get_connection():
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
        connection = deepgram.listen.websocket.v("1")

        return connection