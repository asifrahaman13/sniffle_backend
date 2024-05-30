from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        # List of active connections
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        # Accept the connection
        await websocket.accept()

        # Append the connection to the list of active connections
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):

        # Remove the connection from the list of active connections
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):

        # Send the message to the websocket
        await websocket.send_json(message)

    async def broadcast(self, message: str):

        # Send the message to all active connections
        for connection in self.active_connections:

            # Send the message
            await connection.send_text(message)
