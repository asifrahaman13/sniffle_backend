import base64
from pydub.playback import play
import re
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
import os

load_dotenv()

deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
assert deepgram_api_key, "Deepgram API key is not set"


class VoiceRepository:

    def __init__(self) -> None:
        pass

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
            from deepgram import DeepgramClient, SpeakOptions

            # Create a Deepgram client using the API key
            deepgram = DeepgramClient(api_key=deepgram_api_key)

            # Choose a model to use for synthesis
            options = SpeakOptions(
                model="aura-luna-en",  # Specify the desired voice
                # encoding="aac"  # Specify the desired audio format
            )

            speak_options = {"text": text}

            # Synthesize audio and stream the response
            response = deepgram.speak.v("1").stream(speak_options, options)

            # Get the audio stream from the response
            audio_buffer = response.stream

            # Read the audio data from the buffer and encode it as base64
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            print(type(audio_base64))

            # Reset the audio buffer for reading
            audio_buffer.seek(0)

            return audio_base64

def main():

    input_text = "Sanple text to be converted to speech."
    # Chunk the text into smaller parts

    text_to_speech = VoiceRepository()
    chunks = text_to_speech.chunk_text_by_sentence(input_text)

    # Synthesize each chunk into audio and play the audio
    for chunk_text in chunks:
        audio = text_to_speech.voice_response(chunk_text)
        play(audio)


if __name__ == "__main__":
    main()
