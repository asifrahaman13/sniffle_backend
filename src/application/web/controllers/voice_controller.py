import logging
from fastapi import APIRouter, Depends, WebSocket
from src.infastructure.repositories.chat_repository import ChatResponseRepository
from src.internal.use_cases.chat_service import ChatService
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.chat_interface import ChatInterface

from src.infastructure.repositories.voice_repository import VoiceRepository
from src.internal.use_cases.voice_service import VoiceService
from src.internal.interfaces.voice_interface import VoiceInterface

chat_repository = ChatResponseRepository()
chat_service = ChatService(chat_repository)

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

voice_repository = VoiceRepository()
voice_service = VoiceService(voice_repository)

voice_router = APIRouter()

@voice_router.websocket("/voice/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str,  chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service), voice_interface: VoiceInterface = Depends(voice_service)):
    user_info = auth_interface.decode_access_token(client_id)
    print(user_info)
    await websocket.accept()
    messages_received=[]

    try:
        while True:
            message = await websocket.receive_json()
            logging.info(f"Client #{client_id} sent: {message}")

            messages_received.append({"role": "user", "content": message["query"]})
            
            """
            The streaming response from the chat interface is passed to the voice interface to generate a voice response.
            """
            print("messages received", messages_received)
            llm_streaming_response=chat_interface.streaming_llm_response(user_info["sub"], message["query"], messages_received)


            gen=llm_streaming_response

            while True:
                try:
                    sentences=next(gen)
                    sentences=sentences["response"]
                    print("llm_streaming_response", sentences)
                    text_to_audio_base64=voice_interface.voice_response(sentences)
                    await websocket.send_text(text_to_audio_base64)
                    # messages_received=[]
                except StopIteration:
                    break
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await websocket.close()