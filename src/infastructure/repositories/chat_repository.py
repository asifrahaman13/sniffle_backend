import json
import time
from openai import OpenAI
import logging
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from src.internal.helper.regular_expression import detect_summary
from src.internal.entities.health_model import (
    HealthData,
    Recommendations,
    GeneralParameters,
)
from config.config import OPEN_AI_API_KEY
from src.constants.prompts.prompts import Prompts


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class HealthAssistant:
    def __init__(self):
        self.__model = "gpt-4o"
        self.__openai_api_key = OPEN_AI_API_KEY
        self.__max_tokens = 3000
        self.chat_model = ChatOpenAI(
            model=self.__model,
            openai_api_key=self.__openai_api_key,
            max_tokens=self.__max_tokens,
        )

    def process_output(self, output):

        # Extract the JSON content
        json_content = output.content.strip("```json\n").strip("```")
        try:
            return json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return None

    def format_input(self, user_query):

        # Create a prompt
        parser = PydanticOutputParser(pydantic_object=HealthData)

        # Create a prompt
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                    "\n \n{question}".format(Prompts.HEALTH_ASSISTANT_FORMAT_PROMPT.value)
                )
            ],
            # Define the input variables
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return prompt.format_prompt(question=user_query)

    def format_recommendations(self, user_query):

        # Create a prompt
        parser = PydanticOutputParser(pydantic_object=Recommendations)

        # Create a prompt
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                    "{} \n \n{question}".format(Prompts.FORMAT_RECOMMENDATIONS.value)
                )
            ],
            # Define the input variables
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return prompt.format_prompt(question=user_query)

    def format_user_general_metrics(self, user_query):

        # Create a prompt
        parser = PydanticOutputParser(pydantic_object=GeneralParameters)

        # Create a prompt
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                    "{} \n \n{question}".format(Prompts.FORMAT_USER_GENERAL_METRICS_PROMPT.value)
                )
            ],
            # Define the input variables
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        return prompt.format_prompt(question=user_query)

    def run_health_assistant(self, user_query):

        # Format the input
        input_prompt = self.format_input(user_query)

        # Invoke the model
        output = self.chat_model.invoke(input_prompt.to_messages())

        # Process the output
        return self.process_output(output)

    def run_recommendation_assistant(self, user_query):

        # Format the input
        input_prompt = self.format_recommendations(user_query)

        # Invoke the model
        output = self.chat_model.invoke(input_prompt.to_messages())

        logging.info(
            "The output is",
            output,
        )
        # Process the output
        return self.process_output(output)

    def run_user_general_metrics(self, user_query):

        # Format the input
        input_prompt = self.format_user_general_metrics(user_query)

        # Invoke the model
        output = self.chat_model.invoke(input_prompt.to_messages())

        # Process the output
        return self.process_output(output)


class ChatResponseRepository:

    def __init__(self) -> None:
        self.__temperature = 0.7
        self.__max_tokens = 3000
        self.__model = "gpt-4o"
        self.__client = OpenAI(api_key=OPEN_AI_API_KEY)

    def chat_response(self, _query, previous_messages=[]):

        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.CHAT_RESPONSE.value,
            },
        )

        # Create a completion
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Get the response
        response = response.choices[0].message.content

        # Check if the response is a summary
        if detect_summary(response):
            assistant = HealthAssistant()
            health_data = assistant.run_health_assistant(response)
            logging.info(health_data)

            return {
                "summary": True,
                "response": response,
                "response_schema": health_data,
            }

        return {"summary": False, "response": response}

    def llm_assessment(self, _query, previous_messages=[]):

        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.LLM_ASSESSMENT.value,
            },
        )

        # Create a completion
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Get the response
        response = response.choices[0].message.content

        if detect_summary(response):
            logging.info("Detected sunmmary ...")

            summary = {"summary": response}

            # Extract the JSON content and return the data.
            return {
                "summary": True,
                "response": response,
                "response_schema": summary,
            }

        return {"summary": False, "response": response}

    def llm_recommendation(self, *args):
        messages = []

        for item in args:
            messages.append(
                {
                    "role": "user",
                    "content": f"The quantitave data is as follows: {str(item)}",
                },
            )
        messages.append(
            {
                "role": "system",
                "content": Prompts.LLM_RECOMMENDATION.value,
            },
        )

        # Create a completion
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Get the response
        response = response.choices[0].message.content

        logging.info("LLM response is ready ...")

        assistant = HealthAssistant()
        # Extract the JSON content and return the data.
        recommendations = assistant.run_recommendation_assistant(response)

        summary = {"recommendations": recommendations}

        return summary

    def llm_user_general_metrics(self, _query, previous_messages=[]):
        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.LLM_USER_GENERAL_METRICS.value,
            },
        )

        # Create a completion
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Get the response
        response = response.choices[0].message.content

        if detect_summary(response):
            assistant = HealthAssistant()
            general_metrics = assistant.run_user_general_metrics(response)
            logging.info(general_metrics)

            return {
                "summary": True,
                "response": response,
                "response_schema": general_metrics,
            }

        return {"summary": False, "response": response}

    def streaming_llm_response(self, _query, previous_messages=[]):

        messages = previous_messages.copy()
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.STREAMING_LLM_RESPONSE.value,
            },
        )
        # Record the start time
        start_time = time.time()

        # Create a completion
        stream = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            stream=True,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Initialize a buffer to store the sentence
        sentence_buffer = ""

        total_text = ""
        # Iterate over the stream of chunks
        for chunk in stream:

            # Check if the completion is a message
            if chunk.choices[0].delta.content is not None:

                # Append the chunk to the buffer
                sentence_buffer += chunk.choices[0].delta.content

                total_text += chunk.choices[0].delta.content

                # Check if the sentence is complete
                if sentence_buffer.endswith((".", "!", "?")):
                    # Record the end time
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time

                    logging.info(f"Elapsed time for open ai: {elapsed_time} seconds")

                    # Yield the sentence

                    print("Sending", {"response": total_text, "is_last": True})
                    yield {
                        "response": sentence_buffer.strip(),
                        "is_last": False,
                    }
                    sentence_buffer = ""

        previous_messages.append({"role": "system", "content": total_text})

        if detect_summary(total_text):
            json_parased_quanitative_data = {"summary": total_text}
            print(
                "Sending",
                {
                    "response": total_text,
                    "is_last": True,
                    "response_schema": json_parased_quanitative_data,
                },
            )
            yield {
                "response": total_text,
                "is_last": True,
                "response_schema": json_parased_quanitative_data,
            }

    def streaming_voice_assessment_response(self, _query, previous_messages=[]):

        messages = previous_messages.copy()
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.STREAMING_VOICE_ASSESSMENT_RESPONSE.value,
            },
        )
        # Record the start time
        start_time = time.time()

        # Create a completion
        stream = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            stream=True,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Initialize a buffer to store the sentence
        sentence_buffer = ""

        total_text = ""
        # Iterate over the stream of chunks
        for chunk in stream:

            # Check if the completion is a message
            if chunk.choices[0].delta.content is not None:

                # Append the chunk to the buffer
                sentence_buffer += chunk.choices[0].delta.content

                total_text += chunk.choices[0].delta.content

                # Check if the sentence is complete
                if sentence_buffer.endswith((".", "!", "?")):
                    # Record the end time
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time

                    logging.info(f"Elapsed time for open ai: {elapsed_time} seconds")
                    print("Sending", {"response": total_text, "is_last": True})
                    yield {
                        "response": sentence_buffer.strip(),
                        "is_last": False,
                    }
                    sentence_buffer = ""

        previous_messages.append({"role": "system", "content": total_text})
        if detect_summary(total_text):
            json_parased_quanitative_data = {"summary": total_text}
            print(
                "Sending",
                {
                    "response": total_text,
                    "is_last": True,
                    "response_schema": json_parased_quanitative_data,
                },
            )
            yield {
                "response": total_text,
                "is_last": True,
                "response_schema": json_parased_quanitative_data,
            }

    def get_fhir_data(self, encoded_image):
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": Prompts.FHIR_PROMPT.value,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                        },
                    ],
                }
            ],
            max_tokens=self.__max_tokens,
        )

        result = response.choices[0].message.content
        return result

    def general_chat_query(self, query, previous_messages):
        messages = previous_messages.copy()
        messages.append(
            {"role": "user", "content": query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.GENERAL_CHAT_QUERY.value,
            },
        )

        # Create a completion
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Get the response
        response = response.choices[0].message.content
        return {"response": response}

    def get_streaming_voice_response(self, _query, previous_messages=[]):

        messages = previous_messages.copy()
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": Prompts.GENERAL_STRAMING_VOICE_RESPONSE.value,
            },
        )
        # Record the start time
        start_time = time.time()

        # Create a completion
        stream = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            stream=True,
            max_tokens=self.__max_tokens,
            temperature=self.__temperature,
        )

        # Initialize a buffer to store the sentence
        sentence_buffer = ""
        total_text = ""

        # Iterate over the stream of chunks
        for chunk in stream:

            # Check if the completion is a message
            if chunk.choices[0].delta.content is not None:

                # Append the chunk to the buffer
                sentence_buffer += chunk.choices[0].delta.content

                total_text += chunk.choices[0].delta.content

                # Check if the sentence is complete
                if sentence_buffer.endswith((".", "!", "?")):
                    # Record the end time
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time

                    logging.info(f"Elapsed time for open ai: {elapsed_time} seconds")
                    yield {"response": sentence_buffer.strip()}
                    sentence_buffer = ""

        previous_messages.append({"role": "system", "content": total_text})
