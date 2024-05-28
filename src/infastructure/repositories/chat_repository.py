import json
from openai import OpenAI
import logging
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from src.internal.helper.regular_expression import detect_summary
from src.internal.entities.health_model import HealthData, Recommendations
from config.config import OPEN_AI_API_KEY


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class HealthAssistant:
    def __init__(self):
        self.model = "gpt-4o"
        self.openai_api_key = OPEN_AI_API_KEY
        self.max_tokens = 2500
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
                    "Format the user query into the schema provided to you. It will have systol_blood_pressure and diastol_blood_pressure  pressure (give them separate), heart_rate, respiratory_rate, bod_temperature, step_count, body_temperature, calories_burned, distance_travelled, sleep_duration, water_consumed, caffeine_consumed, alchohol_consumed. Only numerical values to consider no unit\n \n{question}"
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
                "content": "You are a helpful and friendly assistant as if you are the best friend of the user. Your task is to extract the details of heart rate, bood pressure, respiratory rate, blood temperature, step count, calories burnt, distance travelled, sleep duration, water consumed, cofeine_consumed, alchohol consumed etc. You have the previous conversation with the user. Ask follow up questions if the user has not provided enough. Ask no more than two entities at a time. If the details are already provided then you can say 'Summary ready !' and give the summary of the details with the standard units and end the conversation.",
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

    def llm_recommendation(self, general_metrics, assessment_metrics):
        messages = []
        messages.append(
            {"role": "user", "content": str(general_metrics)},
        )
        messages.append(
            {"role": "user", "content": str(assessment_metrics)},
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


if __name__ == "__main__":
    chat_response = ChatResponseRepository()
    gen = chat_response.llm_recommendation(
        "blood pressure 180/78, respiration 90",
        "Here's a summary of the details you've shared:- **Current Feeling**: Fine but experiencing stress - **Stress Cause**: Heavy worklo- **Mood Changes**: Significant changes noticed.- **Sleep Quality**: Reduced from 8 hours to 6 hours.- **Daytime Feeling**: Quite tired and frustrated.- **Anxiety**: Present, espcially during peak workload in the afternoon.- **Strategies Used**: None currently, but interested in trying exercise, meditation, time management, healthy diet, sleep hygiene, talking to someone, and hobbies.I'm glad you're willing to try some new strategies to manage your stress and anxiety. If you need any further assistance or support, feel free to reach out. Take care!",
    )

    print(f"\n\n\n\n\n\nThe final result is", gen)
