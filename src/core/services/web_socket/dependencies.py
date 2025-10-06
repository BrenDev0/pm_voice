from src.core.services.web_socket.services.transport import WebSocketTranportService

def get_ws_transport_service() -> WebSocketTranportService:
    return WebSocketTranportService()