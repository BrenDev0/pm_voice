from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket, status, WebSocketDisconnect, Depends
from uuid import UUID
import json
from langgraph.graph.state import CompiledStateGraph
import base64
from src.workflows.graph import create_graph

from src.shared.services.web_socket.services.connections import WebsocketConnectionsContainer
from src.api.middleware.hmac_verification import verify_hmac_ws
from src.shared.services.speech.domain.speech_to_text import SpeechToText
from src.shared.dependencies.services import get_speech_to_text_service

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

@app.websocket("/ws/{connection_id}")
async def websocket_interact(
    websocket: WebSocket, 
    chat_id: UUID,
    speech_to_text_service: SpeechToText = Depends(get_speech_to_text_service),
    graph: CompiledStateGraph = Depends(create_graph)
):
    await websocket.accept()
    params = websocket.query_params
    signature = params.get("x-signature")
    payload = params.get("x-payload")

    if not await verify_hmac_ws(signature, payload):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    WebsocketConnectionsContainer.register_connection(chat_id, websocket)
    
    print(f'Websocket connection: {chat_id} opened.')

    audio_chunks = []
    try:
        while True: 
            message = await websocket.receive_text()
            data = json.loads(message)
            message_type = data.get("type")

            if message_type == "audio_chunk":
                audio_chunks.append(audio_chunks)
            else: 
                websocket.send_json("Unsuppoerted content")
            
            if audio_chunks:
                async def audio_stream():
                    for chunk in audio_chunks:
                        yield chunk
                
                transcribed_text = await speech_to_text_service.transcribe(audio_stream())
                

    except WebSocketDisconnect:
        print(transcribed_text, "::::Text:::::::::::")
        WebsocketConnectionsContainer.remove_connection(chat_id)
        print(f'Websocket connection: {chat_id} closed.')