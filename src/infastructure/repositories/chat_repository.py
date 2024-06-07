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


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class HealthAssistant:
    def __init__(self):
        self.model = "gpt-4o"
        self.openai_api_key = OPEN_AI_API_KEY
        self.max_tokens = 3000
        self.chat_model = ChatOpenAI(
            model=self.model,
            openai_api_key=self.openai_api_key,
            max_tokens=self.max_tokens,
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
                    "Format the user query into the schema provided to you. It will have systol_blood_pressure and diastol_blood_pressure  pressure (give them separate), heart_rate, respiratory_rate, bod_temperature, step_count, body_temperature, calories_burned, distance_travelled, sleep_duration, water_consumed, caffeine_consumed, alcohol_consumed. Only numerical values to consider no unit. If some data is not provided then use the default value as 0\n \n{question}"
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
                    """Format the user query into the json schema provided to you. It will have medications_recommended, diet_recommended, exercise_recommended, lifestyle_changes_recommended, stress_management_techniques_recommended, sleep_hygiene_techniques_recommended, mental_health_techniques_recommended,  relaxation_techniques_recommended, social_support_techniques_recommended, other_recommendations. Each of the entity should have only two subheader ie 'title' and 'details' only.
                    The user query is as follows: 

                     \n \n{question}"""
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
                    "Format the user query into the schema provided to you. It will have weight, age, current_medications, allergies, previous_mediacal_history, family_medical_history, height, surgical_history, lifestyle, social_history, reproductive_health. The quantitative values should be without any units. The query is as follows: \n \n{question}"
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
        self.temperature = 0.7
        self.max_tokens = 3000
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
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. Your task is to extract the details of heart rate, bood pressure, respiratory rate, blood temperature, step count, calories burnt, distance travelled, sleep duration, water consumed, cofeine_consumed, alcohol consumed etc. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. Ask no more than one entity at a time. If the details are already provided then you can say 'Summary ready !' and give the summary of the details with the standard units and end the conversation.",
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
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. Your task is to ask follow up questions to the users to get meaninful insights on mental health,, stress level, mood, anxiety level, sleep quality. If some data needs more clarification ask followup questions. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. Ask no more than one entities at a time. If the user does not wish to question anymore or the user have provided enough information ie total number of follow up questions exceeds 10 (ten) then you can say 'Summary ready !' and give the summary of the details with the standard units and end the conversation.",
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

        if detect_summary(response):
            logging.info("Detected sunmmary ...")

            summary = {"summary": response}

            # Extract the JSON content and return the data.
            return {"summary": True, "response": response, "response_schema": summary}

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
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. You have the data of the user in the conversation. Your task is to give a detailed recommendation to the users what they should do to improve their health level. You should give output in the following parameters: medications recommended, diet recommended, exercise recommended, lifestyle changes recommended, stress management techniques recommended, sleep hygiene techniques recommended, mental health techniques recommended, relaxation techniques recommended, social support techniques recommended, other recommendations. ",
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
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user.  Your task is to extract the details of weight, age, current_medications, allergies, previous_mediacal_history, family_medical_history, lifestyle, height, surgical_history, social_history, reproductive_health etc. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. Ask no more than one entities at a time. If the details are already provided then you can say 'Summary ready !' and give the summary of the details with the standard units and end the conversation.",
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

        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. Your task is to extract the details of heart rate, bood pressure, respiratory rate, blood temperature, step count, calories burnt, distance travelled, sleep duration, water consumed, cofeine_consumed, alcohol consumed etc. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. Ask no more than one entity at a time. If the details are already provided then you can first say 'Summary ready !' and after that give the summary of the details with the standard units and end the conversation.",
            },
        )
        # Record the start time
        start_time = time.time()

        # Create a completion
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
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
                    yield {"response": sentence_buffer.strip(), "is_last": False}
                    sentence_buffer = ""

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

        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. Your task is to ask follow up questions to the users to get meaninful insights on mental health,, stress level, mood, anxiety level, sleep quality. If some data needs more clarification ask followup questions. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. Ask no more than one entities at a time. If the user does not wish to question anymore or the user have provided enough information ie total number of follow up questions exceeds 10 (ten) then you can say 'Summary ready !' and give the summary of the details with the standard units and end the conversation.",
            },
        )
        # Record the start time
        start_time = time.time()

        # Create a completion
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
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
                    yield {"response": sentence_buffer.strip(), "is_last": False}
                    sentence_buffer = ""

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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Generate FHIR file format from the image. The output should be in the standard FHIR in json format. Ensure that the output is correctly formatted json. Only give the json result with full accuracy which can be converted into json object.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                        },
                    ],
                }
            ],
            max_tokens=self.max_tokens,
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
                "content": "You are a helpful and friendly healthcare assistant as if you are the best friend of the user. Your task is answer the query of the user in a very friendly manner. Use emoji whenever required.",
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
        return {"response": response}

    def get_streaming_voice_response(self, _query, previous_messages=[]):

        messages = previous_messages
        messages.append(
            {"role": "user", "content": _query},
        )
        messages.append(
            {
                "role": "system",
                "content": "You are a helpful and friendly healthcare assistant as if you are the best friend of the user. Your task is answer the query of the user in a very friendly manner.",
            },
        )
        # Record the start time
        start_time = time.time()

        # Create a completion
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        # Initialize a buffer to store the sentence
        sentence_buffer = ""

        # Iterate over the stream of chunks
        for chunk in stream:

            # Check if the completion is a message
            if chunk.choices[0].delta.content is not None:

                # Append the chunk to the buffer
                sentence_buffer += chunk.choices[0].delta.content

                # Check if the sentence is complete
                if sentence_buffer.endswith((".", "!", "?")):
                    # Record the end time
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time

                    logging.info(f"Elapsed time for open ai: {elapsed_time} seconds")
                    yield {"response": sentence_buffer.strip()}
                    sentence_buffer = ""
