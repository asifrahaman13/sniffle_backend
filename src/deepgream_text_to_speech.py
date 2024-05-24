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


class TextToSpeech:

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

    def synthesize_audio(self, text):
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

        # # Load audio from buffer using pydub
        # audio = AudioSegment.from_mp3(audio_buffer)

        # # Play the audio
        # play(audio)
        # # time.sleep(15)

        # Reset the audio buffer for reading
        audio_buffer.seek(0)

        # Read the audio data from the buffer
        # audio_data = audio_buffer.read()

        return audio_buffer


def main():

    input_text = ""
    # Chunk the text into smaller parts

    text_to_speech = TextToSpeech()
    chunks = text_to_speech.chunk_text_by_sentence(input_text)

    # Synthesize each chunk into audio and play the audio
    for chunk_text in chunks:
        audio = text_to_speech.synthesize_audio(chunk_text)
        play(audio)


if __name__ == "__main__":
    main()
