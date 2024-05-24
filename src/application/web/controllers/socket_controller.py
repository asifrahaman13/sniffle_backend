
import logging
from fastapi import WebSocket, APIRouter
from src.open_ai_llm_response import ChatResponse
from src.ConnectionManager.ConnectionManager import ConnectionManager
from fastapi import  WebSocket, WebSocketDisconnect

# Create a router for the websocket
websocket_router=APIRouter()

# Create a connection manager
manager = ConnectionManager()

@websocket_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):

    # Connect the websocket
    await manager.connect(websocket)
    try:
        while True:
            # Wait for the message from the client
            data = await websocket.receive_text()

            # Log the message
            logging.info(f"Client #{client_id} sent: {data}")

            # Create a chat response
            _chat_response=ChatResponse()

            # Get the response
            response= _chat_response.chat_response(data)
            
            # Send the response to the client
            await manager.send_personal_message(str(response), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

