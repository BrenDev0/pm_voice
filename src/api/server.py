from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket, status, WebSocketDisconnect, Depends
from uuid import UUID
import json
from langgraph.graph.state import CompiledStateGraph
import base64

from src.shared.application.use_cases.stream_tts import StreamTTS
from src.shared.dependencies.services import get_stream_tts_use_case
from src.shared.dependencies.configure_container import configure_container
from src.api.services.state_service import StateService
from src.workflows.graph import create_graph
from src.api.websocket.connections import WebsocketConnectionsContainer
from src.api.middleware.hmac_verification import verify_hmac_ws
from src.shared.domain.speech_to_text import SpeechToText
from src.shared.dependencies.services import get_speech_to_text_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_container()  
    yield


app = FastAPI(lifespan=lifespan)

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
    connection_id: UUID,
    websocket: WebSocket,
    speech_to_text_service: SpeechToText = Depends(get_speech_to_text_service),
    graph: CompiledStateGraph = Depends(create_graph),
    greeting: StreamTTS = Depends(get_stream_tts_use_case)
):
    await websocket.accept()
    
    params = websocket.query_params
    # signature = params.get("x-signature")
    # payload = params.get("x-payload")

    # if not await verify_hmac_ws(signature, payload):
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     return

    connection_id = params.get("connection_id", connection_id)
    if not connection_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing connection_id")
        return
    

    WebsocketConnectionsContainer.register_connection(connection_id, websocket)
    
    print(f'Websocket connection: {connection_id} opened.')
    

    await greeting.execute(
        ws_connection_id=connection_id,
        text="""
        Gracias para llamar Propiedades  mérida! ¿En cómo te puedo ayudar?
        """ 
    )
    
    transcription_session = None
    state = StateService.get_new_state(connection_id)
    
    try:
        while True: 
            message = await websocket.receive()
            if "bytes" in message:
                if transcription_session:
                    await speech_to_text_service.send_audio_chunk(transcription_session, message["bytes"])

            elif "text" in message:
                data = json.loads(message["text"])
                message_type = data.get("type")

                if message_type == "audio_start":
                    print("START")
                    transcription_session = await speech_to_text_service.start_transcription_session()

                elif message_type == "audio_end":
                    print("END")
                    transcription = await speech_to_text_service.end_transcription_session(transcription_session)
                    transcription_session = None
                    
                    state = StateService.refresh_turn(
                        state=state,
                        input=transcription
                    )

                    with open("./src/public/keyboard-typing-329937.mp3", "rb") as f:
                        audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

                    await websocket.send_json({
                        "type": "audio_response",
                        "audio_data": audio_base64,
                        "format": "mp3"
                    })

                    final_state = await graph.ainvoke(state)
                    
                    state = StateService.update_chat_history(
                        state=state,
                        input=final_state["input"],
                        response=final_state["response"]
                    )
                    


    except WebSocketDisconnect:
        if transcription_session:
            await speech_to_text_service.cleanup_session(transcription_session)
            WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)
        print("Connection closed")
    except Exception as e:
        print("ERROR::::::", e)
        if transcription_session:
            await speech_to_text_service.cleanup_session(transcription_session)