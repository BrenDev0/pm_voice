from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect, Depends
from uuid import UUID
from langgraph.graph.state import CompiledStateGraph

from src.workflows.graph import create_graph

from src.shared.services.web_socket.services.connections import WebsocketConnectionsContainer
from src.api.middleware.hmac_verification import verify_hmac_ws

router = APIRouter(
    tags=["WebSocket"]
)

@router.websocket("/internal/interact/{chat_id}")
async def websocket_interact(
    websocket: WebSocket, 
    chat_id: UUID,
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
    try:
        while True: 
            await websocket.receive_text()

    except WebSocketDisconnect:
        WebsocketConnectionsContainer.remove_connection(chat_id)
        print(f'Websocket connection: {chat_id} closed.')