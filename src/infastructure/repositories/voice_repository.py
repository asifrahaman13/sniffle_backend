from deepgram import DeepgramClient, SpeakOptions
import base64
import re
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)
from dotenv import load_dotenv
import os

load_dotenv()

deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
assert deepgram_api_key, "Deepgram API key is not set"


class VoiceRepository:

    def __init__(self) -> None:
        self.__model="aura-luna-en"

    def chunk_text_by_sentence(self, text):

        # Find sentence boundaries using regular expression
        sentence_boundaries = re.finditer(r"(?<=[.!?])\s+", text)

        # Get the indices of the sentence boundaries
        boundaries_indices = [boundary.start() for boundary in sentence_boundaries]

        chunks = []
        start = 0
        # Split the text into chunks based on sentence boundaries
        for boundary_index in boundaries_indices:

            # Add the chunk to the list
            chunks.append(text[start : boundary_index + 1].strip())

            # Update the start index for the next chunk
            start = boundary_index + 1

        # Add the remaining text as the last chunk
        chunks.append(text[start:].strip())

        return chunks

    def voice_response(self, text):

        # Create a Deepgram client using the API key
        deepgram = DeepgramClient(api_key=deepgram_api_key)

        # Choose a model to use for synthesis
        options = SpeakOptions(
            model=self.__model,  # Specify the desired voice
            # encoding="aac"  # Specify the desired audio format
        )

        speak_options = {"text": text}

        # Synthesize audio and stream the response
        response = deepgram.speak.v("1").stream(speak_options, options)

        # Get the audio stream from the response
        audio_buffer = response.stream

        # Read the audio data from the buffer and encode it as base64
        audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")

        # Reset the audio buffer for reading
        audio_buffer.seek(0)

        return audio_base64
