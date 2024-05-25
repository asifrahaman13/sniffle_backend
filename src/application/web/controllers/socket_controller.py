import logging
from fastapi import WebSocket, APIRouter, Depends
from src.ConnectionManager.ConnectionManager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
from src.infastructure.repositories.chat_repository import ChatResponseRepository
from src.internal.use_cases.chat_service import ChatService

chat_repository = ChatResponseRepository()
chat_service = ChatService(chat_repository)

# Create a router for the websocket
websocket_router = APIRouter()

# Create a connection manager
manager = ConnectionManager()


@websocket_router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, client_id: str, chat_interface=Depends(chat_service)
):
    # Connect the websocket
    await manager.connect(websocket)

    try:
        while True:
            # Wait for the message from the client
            data = await websocket.receive_json()
            

            logging.info(type(data))

            # Log the message
            logging.info(f"Client #{client_id} sent: {data}")

            # Create a chat response
            chat_response = chat_interface.chat_response(data['query'])

            # Send the response to the client
            await manager.send_personal_message(chat_response, websocket)
          
    except WebSocketDisconnect:

        # Disconnect the websocket
        manager.disconnect(websocket)
        # Broadcast the message to all clients
        await manager.broadcast(f"Client #{client_id} left the chat")
