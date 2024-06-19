import logging
from fastapi import APIRouter, Depends, WebSocket
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.chat_interface import ChatInterface
from src.internal.interfaces.voice_interface import VoiceInterface
from exports.exports import chat_service, auth_service, voice_service, manager

voice_router = APIRouter()

@voice_router.websocket("/voice_health_metrics/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
    voice_interface: VoiceInterface = Depends(voice_service),
):
    user_info = auth_interface.decode_access_token(client_id)
    logging.info(user_info)
    # Connect the websocket
    await manager.connect(websocket, client_id, "voice")

    messages_received = []

    try:
        while True:
            message = await websocket.receive_json()
            logging.info(f"Client #{client_id} sent: {message}")

            messages_received.append({"role": "user", "content": message["query"]})

            """
            The streaming response from the chat interface is passed to the voice interface to generate a voice response.
            """
            logging.info("messages received")
            logging.info(messages_received)
            llm_streaming_response = chat_interface.streaming_llm_response(
                user_info["sub"], message["query"], messages_received
            )

            gen = llm_streaming_response

            while True:
                try:
                    sentences = next(gen)
                    sentences = sentences["response"]
                    logging.info("llm_streaming_response")
                    logging.info(sentences)
                    text_to_audio_base64 = voice_interface.voice_response(sentences)
                    await manager.send_personal_message(text_to_audio_base64, websocket)
                    # messages_received=[]
                except StopIteration:
                    break

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await manager.disconnect(websocket)


@voice_router.websocket("/voice_assessment/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
    voice_interface: VoiceInterface = Depends(voice_service),
):
    user_info = auth_interface.decode_access_token(client_id)
    logging.info(user_info)
    await manager.connect(websocket, client_id, "voice")
    messages_received = []

    try:
        while True:
            message = await websocket.receive_json()
            logging.info(f"Client #{client_id} sent: {message}")

            messages_received.append({"role": "user", "content": message["query"]})

            """
            The streaming response from the chat interface is passed to the voice interface to generate a voice response.
            """
            logging.info("messages received")
            logging.info(messages_received)
            llm_streaming_response = chat_interface.streaming_voice_assessment_response(
                user_info["sub"], message["query"], messages_received
            )

            gen = llm_streaming_response

            while True:
                try:
                    sentences = next(gen)
                    sentences = sentences["response"]
                    logging.info("llm_streaming_response")
                    logging.info(sentences)
                    text_to_audio_base64 = voice_interface.voice_response(sentences)
                    await manager.send_personal_message(text_to_audio_base64, websocket)
                    # messages_received=[]
                except StopIteration:
                    break

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await manager.disconnect(websocket)


@voice_router.websocket("/general_voice_response/{client_id}")
async def websocket_endpoint_query(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
    voice_interface: VoiceInterface = Depends(voice_service),
):
    user_info = auth_interface.decode_access_token(client_id)
    logging.info(user_info)
    await manager.connect(websocket, client_id, "voice")
    messages_received = []

    try:
        while True:
            message = await websocket.receive_json()
            logging.info(f"Client #{client_id} sent: {message}")

            messages_received.append({"role": "user", "content": message["query"]})

            """
            The streaming response from the chat interface is passed to the voice interface to generate a voice response.
            """
            logging.info("messages received")
            logging.info(messages_received)
            llm_streaming_response = chat_interface.get_streaming_voice_response(
                message["query"], messages_received
            )

            gen = llm_streaming_response

            while True:
                try:
                    sentences = next(gen)
                    sentences = sentences["response"]
                    logging.info("llm_streaming_response")
                    logging.info(sentences)
                    text_to_audio_base64 = voice_interface.voice_response(sentences)
                    await manager.send_personal_message(text_to_audio_base64, websocket)
                    # messages_received=[]
                except StopIteration:
                    break

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await manager.disconnect(websocket)
