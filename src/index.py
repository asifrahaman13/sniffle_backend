import asyncio
import websockets
from deepgream_text_to_speech import TextToSpeech
from open_ai_llm_response import ChatResponse
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def echo(websocket, path):
    messages_received = []

    # Iterate over the messages received from the client
    async for message in websocket:

        # Append the message to the list
        messages_received.append(message)

        # Check if the list has only one message
        if len(messages_received) == 1:
            # Record the start time
            start_time = time.time()

            # Compile the messages into a single text
            compiled_text = " ".join(messages_received)

            # Create a chat response object
            chat_response = ChatResponse()

            # Get the chat response
            _chat_response = chat_response.chat_response(compiled_text)

            gen = _chat_response
            while True:
                try:
                    sentences = next(gen)
                    logging.info(f"Received sentence: {sentences}")

                    # Create a text to speech object
                    text_to_speech = TextToSpeech()
                    audio = text_to_speech.synthesize_audio(sentences)

                    # Record the end time
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time
                    logging.info(
                        f"Elapsed time till receiving audio: {elapsed_time} seconds"
                    )

                    print(type(audio))
                    # Send the audio to the client
                    await websocket.send(audio)

                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time
                    logging.info(
                        f"Elapsed time till after receiving audio: {elapsed_time} seconds"
                    )

                    messages_received = []  # Reset for next set of messages
                except StopIteration:
                    break


async def main():
    try:
        async with websockets.serve(echo, "localhost", 8000):
            logging.info("Server started")
            await asyncio.Future()  # run forever
    except Exception as e:
        logging.error(f"Server error: {e}")
        main()


if __name__ == "__main__":
    asyncio.run(main())
