from src.core.services.web_socket.services.transport import WebSocketTransportService

def get_ws_transport_service() -> WebSocketTransportService:
    return WebSocketTransportService()