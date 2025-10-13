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


from src.workflows.models import State
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

@app.websocket("/ws")
async def websocket_interact(
    websocket: WebSocket,
    speech_to_text_service: SpeechToText = Depends(get_speech_to_text_service),
    graph: CompiledStateGraph = Depends(create_graph)
):
    await websocket.accept()
    # params = websocket.query_params
    # signature = params.get("x-signature")
    # payload = params.get("x-payload")

    # if not await verify_hmac_ws(signature, payload):
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     return


    # params = websocket.query_params
    # connection_id = params.get("connection_id", connection_id)
    
    # if not connection_id:
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing connection_id")
    #     return
    

    WebsocketConnectionsContainer.register_connection(1, websocket)
    
    # print(f'Websocket connection: {connection_id} opened.')
    print("connection opened")
    transcription_session = None
    full_transcript = []
    
    try:
        while True: 
            message = await websocket.receive()
            if "bytes" in message:
                # This is a raw audio chunk
                if transcription_session:
                    print("SEND")
                    print("::::::::::: received audio chunk")
                    await speech_to_text_service.send_audio_chunk(transcription_session, message["bytes"])
            elif "text" in message:
                # This is a JSON control message
                data = json.loads(message["text"])
                message_type = data.get("type")
                if message_type == "audio_start":
                    print("START")
                    transcription_session = await speech_to_text_service.start_transcription_session()
                elif message_type == "audio_end":
                    print("audio end")
                    transcription = await speech_to_text_service.end_transcription_session(transcription_session)
                    transcription_session = None
                    state = State(
                        call_id=1,
                        input=transcription,
                        chat_history=[],
                        summary="",
                        investment_data=None,
                        client_data=None,
                        appointment_data=None
                    )

                    print(state["input"], "INPUT::::::::::::")
                    final_state = await graph.ainvoke(state)
                    print("final state", final_state)


    except WebSocketDisconnect:
        if transcription_session:
            await speech_to_text_service.cleanup_session(transcription_session)
        print("Connection closed")
    except Exception as e:
        print("ERROR::::::", e)
        if transcription_session:
            await speech_to_text_service.cleanup_session(transcription_session)