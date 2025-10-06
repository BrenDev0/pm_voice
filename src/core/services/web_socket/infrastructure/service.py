from fastapi import WebSocket
from typing import Union, Dict
from uuid import UUID

class WebsocketService:
    _active_connections: Dict[str, WebSocket] = {}

    @classmethod
    def add_connection(cls, connection_id: Union[UUID, str], websocket: WebSocket):
        key = str(connection_id)
        cls._active_connections[key] = websocket
        print(f"connection {key} added.")
        return
    
    @classmethod
    def get_connection(cls, connection_id: Union[UUID, str]) -> WebSocket:
        key = str(connection_id)
        connection = cls._active_connections.get(key)
        if not connection:
            print(f"Connection {key} not found in get_connection()")
            return None

        return connection

    @classmethod
    def remove_connection(cls, connection_id: str):
        key = str(connection_id)
        cls._active_connections.pop(key, None)
        print(f'Connection: {key} was removed.')