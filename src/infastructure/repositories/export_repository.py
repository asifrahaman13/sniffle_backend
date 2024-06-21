import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class ExportRepository:

    def __init__(self) -> None:
        pass

    def send_email(self, subject, body, to_email, from_email, from_password):
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(from_email, from_password)
            server.send_message(msg)
            logging.info("Email sent successfully!")

            return True
        except Exception as e:
            logging.info(f"Failed to send email: {e}")
            return False
        finally:
            server.quit()
