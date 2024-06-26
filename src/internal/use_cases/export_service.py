import logging
from src.internal.interfaces.export_interface import ExportInterface
from src.infastructure.repositories.database_repository import DatabaseRepository
from src.infastructure.repositories.export_repository import ExportRepository
from datetime import datetime
from config.config import EMAIL_USERNAME, EMAIL_PASSWORD

"""
Export Service class is responsible for exporting the data from the database and sending it through any 
notification provider. Currently supports exporting the data through registered email.
"""


class ExportService:

    def __call__(self) -> ExportInterface:
        return self

    def __init__(
        self,
        database_repository: DatabaseRepository = DatabaseRepository,
        export_repository: ExportRepository = ExportRepository,
    ) -> None:
        self.__database_repository = database_repository
        self.__export_repository = export_repository
        self.__from_email = EMAIL_USERNAME
        self.__from_password = EMAIL_PASSWORD

    def format_quantitative_data_as_html(self, data):
        email = data["email"]
        records = data["data"]

        html = f"<h2>Health Data for {email}</h2>"
        html += "<table border='1'>"
        html += "<tr><th>Weight</th><th>Sugar Level</th><th>Systolic BP</th><th>Diastolic BP</th><th>Heart Rate</th><th>Respiratory Rate</th><th>Body Temperature</th><th>Step Count</th><th>Calories Burned</th><th>Distance Travelled</th><th>Sleep Duration</th><th>Water Consumed</th><th>Caffeine Consumed</th><th>Alcohol Consumed</th><th>Timestamp</th></tr>"

        for record in records:
            timestamp = record.get("timestamp", "No timestamp provided")
            # Convert timestamp to readable date and time format
            readable_time = datetime.fromtimestamp(timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            html += f"<tr><td>{record.get('weight')}</td><td>{record.get('sugar_level')}</td><td>{record.get('systol_blood_pressure')}</td><td>{record.get('diastol_blood_pressure')}</td><td>{record.get('heart_rate')}</td><td>{record.get('respiratory_rate')}</td><td>{record.get('body_temperature')}</td><td>{record.get('step_count')}</td><td>{record.get('calories_burned')}</td><td>{record.get('distance_travelled')}</td><td>{record.get('sleep_duration')}</td><td>{record.get('water_consumed')}</td><td>{record.get('caffeine_consumed')}</td><td>{record.get('alcohol_consumed')}</td><td>{readable_time}</td></tr>"

        html += "</table>"
        return html

    def format_assessment_data_as_html(self, data):
        email = data["email"]
        records = data["data"]

        html = f"<h2>Health Summary Data for {email}</h2>"
        html += "<table border='1'>"
        html += "<tr><th>Summary</th><th>Timestamp</th></tr>"

        for record in records:
            summary = record.get("summary", "No summary provided")
            timestamp = record.get("timestamp", "No timestamp provided")

            # Convert timestamp to readable date and time format
            readable_time = datetime.fromtimestamp(timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            html += f"<tr><td>{summary}</td><td>{readable_time}</td></tr>"

        html += "</table>"
        return html

    def export_data(self, user: str, collection_name: str):
        try:
            # Find the data from the database.
            data = self.__database_repository.find_single_document(
                "email", user, collection_name
            )

            if collection_name == "quantitative_metrics":
                # If data is present then we need to parse it and send it as an email.
                html_body = self.format_quantitative_data_as_html(data)
                response = self.__export_repository.send_email(
                    "Your Health Data Report",
                    html_body,
                    user,
                    self.__from_email,
                    self.__from_password,
                )
            elif collection_name == "assessment_metrics":
                # If data is present then we need to parse it and send it as an email.
                html_body = self.format_assessment_data_as_html(data)
                response = self.__export_repository.send_email(
                    "Your Health Summary Report",
                    html_body,
                    user,
                    self.__from_email,
                    self.__from_password,
                )

            return response
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return None
