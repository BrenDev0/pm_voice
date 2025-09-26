from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, APIRouter, WebSocket, status, WebSocketDisconnect, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from deepgram import LiveTranscriptionEvents
from fastapi.staticfiles import StaticFiles

from src.dependencies.services import get_deepgram_service
from src.workflow.services.deepgram_service import DeepGramService


app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="src/public"), name="public")

@app.get("/")
async def get():
    return FileResponse('src/public/index.html')

router = APIRouter()

@router.websocket("/ws")
async def websocket_interact(
    websocket: WebSocket,
    deepgram_service: DeepGramService = Depends(get_deepgram_service)
):
    await websocket.accept()
    print("Client connected")
    
    chunks = []
 
    try:
        dg_connection = deepgram_service.get_connection()
        options = deepgram_service.get_options(
            model="nova",
            language="es"
        )
    
        if not dg_connection.start(options):
            print("Failed to start Deepgram connection")
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
            return

        print("Deepgram connection started")

        def on_transcript(self, result, **kwargs):
            try:
                sentence = result.channel.alternatives[0].transcript
                if sentence and len(sentence) > 0:
                    print(f"Transcript: {sentence}")
                    chunks.append(sentence)
            except Exception as e:
                print(f"Error processing transcript: {e}")

        dg_connection.on(LiveTranscriptionEvents.Open, deepgram_service.on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
        dg_connection.on(LiveTranscriptionEvents.Error, deepgram_service.on_error)
        dg_connection.on(LiveTranscriptionEvents.Close, deepgram_service.on_close)

        try: 
            while True:
                data = await websocket.receive_bytes()
                dg_connection.send(data)
        except WebSocketDisconnect:
            print("client disconnect")
            
            if len(chunks) != 0:
                input = " ".join(chunks)
                await websocket.send_text(input)
       

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:     
        if dg_connection:
            try:
                dg_connection.finish()
            except:
                pass
        print("Connection closed")


app.include_router(router)