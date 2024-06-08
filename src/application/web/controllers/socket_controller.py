import logging
from fastapi import WebSocket, APIRouter, Depends
from src.ConnectionManager.ConnectionManager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect
from src.infastructure.repositories.chat_repository import (
    ChatResponseRepository,
)
from src.internal.use_cases.chat_service import ChatService
from src.infastructure.repositories.auth_repository import AuthRepository
from src.internal.use_cases.auth_service import AuthService
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.chat_interface import ChatInterface

chat_repository = ChatResponseRepository()
chat_service = ChatService(chat_repository)

# Create a router for the websocket
websocket_router = APIRouter()

# Create a connection manager
manager = ConnectionManager()

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)


@websocket_router.websocket("/health_metrics/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
):
    # Connect the websocket
    await manager.connect(websocket)

    logging.info(f"Client #{client_id} connected for health metrics")

    user_info = auth_interface.decode_access_token(client_id)

    if user_info is None or "error" in user_info:
        await websocket.send_json("Invalid token")
        return

    all_messages = []

    try:
        while True:
            # Wait for the message from the client
            data = await websocket.receive_json()

            received_data = {"role": "user", "content": data["query"]}
            all_messages.append(received_data)

            logging.info(type(data))

            # Log the message
            logging.info(f"Client #{client_id} sent: {data}")

            # Create a chat response
            chat_response = chat_interface.chat_response(
                user_info["sub"], data["query"], all_messages
            )

            # Log the response
            llm_response = {"role": "system", "content": chat_response}

            # Append the response to the all_messages list
            all_messages.append(llm_response)

            # Send the response to the client
            await manager.send_personal_message(chat_response, websocket)

    except WebSocketDisconnect:

        # Disconnect the websocket
        manager.disconnect(websocket)
        # Broadcast the message to all clients
        await manager.broadcast(f"Client #{client_id} left the chat")


@websocket_router.websocket("/assessment/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
):
    # Connect the websocket
    await manager.connect(websocket)

    logging.info(f"Client #{client_id} connected for assessment")

    user_info = auth_interface.decode_access_token(client_id)

    if user_info is None or "error" in user_info:
        await websocket.send_json("Invalid token")
        return

    all_messages = []

    try:
        while True:
            # Wait for the message from the client
            data = await websocket.receive_json()

            received_data = {"role": "user", "content": data["query"]}
            all_messages.append(received_data)

            logging.info(type(data))

            # Log the message
            logging.info(f"Client #{client_id} sent: {data}")

            # Create a chat response
            chat_response = chat_interface.llm_assessment(
                user_info["sub"], data["query"], all_messages
            )

            # Log the response
            llm_response = {"role": "system", "content": chat_response}

            # Append the response to the all_messages list
            all_messages.append(llm_response)

            # Send the response to the client
            await manager.send_personal_message(chat_response, websocket)

    except WebSocketDisconnect:

        # Disconnect the websocket
        manager.disconnect(websocket)
        # Broadcast the message to all clients
        await manager.broadcast(f"Client #{client_id} left the chat")


@websocket_router.websocket("/general_metrics/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
):
    # Connect the websocket
    await manager.connect(websocket)

    logging.info(f"Client #{client_id} connected for health metrics")

    user_info = auth_interface.decode_access_token(client_id)

    if user_info is None or "error" in user_info:
        await websocket.send_json("Invalid token")
        return

    all_messages = []

    try:
        while True:
            # Wait for the message from the client
            data = await websocket.receive_json()

            received_data = {"role": "user", "content": data["query"]}
            all_messages.append(received_data)

            # Log the message
            logging.info(f"Client #{client_id} sent: {data}")

            # Create a chat response
            chat_response = chat_interface.llm_user_general_metrics(
                user_info["sub"], data["query"], all_messages
            )

            # Log the response
            llm_response = {"role": "system", "content": chat_response}

            # Append the response to the all_messages list
            all_messages.append(llm_response)

            # Send the response to the client
            await manager.send_personal_message(chat_response, websocket)

    except WebSocketDisconnect:

        # Disconnect the websocket
        manager.disconnect(websocket)
        # Broadcast the message to all clients
        await manager.broadcast(f"Client #{client_id} left the chat")


@websocket_router.websocket("/general_chat_reponse/{client_id}")
async def websocket_general_chat(
    websocket: WebSocket,
    client_id: str,
    chat_interface: ChatInterface = Depends(chat_service),
    auth_interface: AuthInterface = Depends(auth_service),
):
    # Connect the websocket
    await manager.connect(websocket)

    logging.info(f"Client #{client_id} connected for health metrics")

    user_info = auth_interface.decode_access_token(client_id)

    if user_info is None or "error" in user_info:
        await websocket.send_json("Invalid token")
        return

    all_messages = []

    try:
        while True:
            # Wait for the message from the client
            data = await websocket.receive_json()

            received_data = {"role": "user", "content": data["query"]}
            all_messages.append(received_data)

            # Log the message
            logging.info(f"Client #{client_id} sent: {data}")

            # Create a chat response
            chat_response = chat_interface.general_chat_query(
                data["query"], all_messages
            )

            # Log the response
            llm_response = {
                "role": "system",
                "content": chat_response["response"],
            }

            # Append the response to the all_messages list
            all_messages.append(llm_response)

            # Send the response to the client
            await websocket.send_json(chat_response["response"])

    except WebSocketDisconnect:
        logging.info(f"Client {client_id} disconnected")

        # Disconnect the websocket
        manager.disconnect(websocket)
        # Broadcast the message to all clients
        # await manager.broadcast(f"Client #{client_id} left the chat")
