import json
from openai import OpenAI
import logging
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from src.internal.helper.regular_expression import detect_summary
from src.internal.entities.health_model import HealthData
from config.config import OPEN_AI_API_KEY


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class HealthAssistant:
    def __init__(self):
        self.model = "gpt-4o"
        self.openai_api_key = OPEN_AI_API_KEY
        self.max_tokens = 300
        self.chat_model = ChatOpenAI(
            model=self.model,
            openai_api_key=self.openai_api_key,
            max_tokens=self.max_tokens,
        )

    def format_input(self, user_query):

        # Create a prompt
        parser = PydanticOutputParser(pydantic_object=HealthData)

        # Create a prompt
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                    "Format the user query into the schema provided to you. It will have systol_blood_pressure and diastol_blood_pressure  pressure (give them separate), heart_rate, respiratory_rate, body_temperature. Only numerical values to consider no unit\n \n{question}"
                )
            ],
            # Define the input variables
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return prompt.format_prompt(question=user_query)

    def process_output(self, output):

        # Extract the JSON content
        json_content = output.content.strip("```json\n").strip("```")
        try:
            return json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return None

    def run_health_assistant(self, user_query):

        # Format the input
        input_prompt = self.format_input(user_query)

        # Invoke the model
        output = self.chat_model.invoke(input_prompt.to_messages())

        # Process the output
        return self.process_output(output)


class ChatResponseRepository:

    def __init__(self) -> None:
        self.temperature = 0.7
        self.max_tokens = 500
        self.model = "gpt-4o"
        self.client = OpenAI(api_key=OPEN_AI_API_KEY)

    def chat_response(self, _query, previous_messages=[]):

        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. Your task is to extract the details of heart rate, bood pressure, respiratory rate, blood temperature etc. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. If the details are already provided then you can say 'Summary ready !' and give the summary of the details with the standard units and end the conversation.",
            },
        )

        # Create a completion
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        # Get the response
        response = response.choices[0].message.content

        # Check if the response is a summary
        if detect_summary(response):
            assistant = HealthAssistant()
            health_data = assistant.run_health_assistant(response)
            logging.info(health_data)

        return response


if __name__ == "__main__":
    chat_response = ChatResponseRepository()
    gen = chat_response.chat_response("Tell me something about India", [])
    while True:
        try:
            sentences = next(gen)
            logging.info(sentences)
        except StopIteration:
            break
