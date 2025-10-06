from deepgram import DeepgramClient, LiveOptions
import os

def on_open(open_event=None):
    print("Deepgram connection open")
  
def on_error(error):
    print(f"Deepgram error: {error}")

def on_close(close_event=None):
    print("Deepgram connection closed")

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
         
def get_connection():
    deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
    connection = deepgram.listen.websocket.v("1")

    return connection