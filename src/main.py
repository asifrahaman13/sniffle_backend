import asyncio
import websockets
from src.deepgream_text_to_speech import TextToSpeech
from src.open_ai_llm_response import ChatResponse
import time
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.ConnectionManager.ConnectionManager import ConnectionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Client #{client_id} sent: {data}")
            _chat_response=ChatResponse()
            response= _chat_response.chat_response(data)

            await manager.send_personal_message(str(response), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
    

if __name__ == "__main__":
    asyncio.run(websockets.serve(websocket_endpoint, "localhost", 8000))
