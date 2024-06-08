import boto3
from config.config import AWS_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY


class AWSRepository:

    """
    Initialize the AWSRepository class with the required configuration.
    """
    def __init__(self):

        self.__aws_bucket_name = AWS_BUCKET_NAME
        self.__aws_access_key = AWS_ACCESS_KEY
        self.__aws_secret_key = AWS_SECRET_KEY
        self.__aws_service = "s3"
        self.__s3_client = boto3.client(
            self.__aws_service,
            aws_access_key_id=self.__aws_access_key,
            aws_secret_access_key=self.__aws_secret_key,
        )
        self.expiration_time = 60

    def upload_json(self, file_name: str, file_content: str):
        try:
            # Upload the file to the S3 bucket
            self.__s3_client.put_object(
                Bucket=self.__aws_bucket_name, Key=file_name, Body=file_content
            )
            return True
        except Exception as e:
            print(e)
            return False

    def get_presigned_json_url(self, file_name: str):
        try:
            # Generate a presigned URL for the file
            url = self.__s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.__aws_bucket_name,
                    "Key": file_name,
                    "ResponseContentDisposition": "inline",
                    "ResponseContentType": "application/json",
                },
                ExpiresIn=self.expiration_time,
            )
            print(url)
            return url
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
