



import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load the environment variables
load_dotenv()

# Create an OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assert client, "OpenAI client is not set"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ChatResponseRepository:

    def __init__(self) -> None:
        self.temperature = 0.7
        self.max_tokens = 150
        self.model= "gpt-4o"

    def chat_response(self, _query):

        # Create a completion
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. help to make the text in points. a. b. etc should be the ordered list bullet points. Your response should be to the point concise and crisp clear.",
                },
                {"role": "user", "content": _query},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        # Get the response
        response =response.choices[0].message.content

        return response

        
if __name__ == "__main__":
    chat_response = ChatResponseRepository()
    gen = chat_response.chat_response("Tell me something about India")
    while True:
        try:
            sentences = next(gen)
            logging.info(sentences)
        except StopIteration:
            break
