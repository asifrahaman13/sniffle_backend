import tempfile
from fastapi import APIRouter, Depends, HTTPException, Header
import json
import logging
import os
import base64
from fastapi import File, Form, UploadFile, HTTPException
from src.internal.entities.export import FileName
from src.internal.interfaces.auth_interface import AuthInterface
from src.internal.interfaces.chat_interface import ChatInterface
from src.internal.interfaces.aws_interface import AWSInterface
from src.internal.interfaces.database_interface import DatabaseInterface
from exports.exports import chat_service, aws_service, database_service, auth_service

fhir_router = APIRouter()


@fhir_router.post("/image-description")
async def get_image_description(
    file: UploadFile = File(...),
    file_name: str = Form(...),
    chat_interface: ChatInterface = Depends(chat_service),
    aws_interface: AWSInterface = Depends(aws_service),
    database_interface: DatabaseInterface = Depends(database_service),
):
    logging.info("started.")
    contents = await file.read()
    encoded_image = base64.b64encode(contents).decode("utf-8")
    logging.info(encoded_image)

    gpt4_description = chat_interface.get_fhir_data(encoded_image)
    logging.info(gpt4_description)

    """
    Extract out the json data from the chat response of the LLM. We need to parse the data later into json format.
    We also need to upload the files into the AWS S3, and 
    save the name of the file in mongodb database. 
    """
    gpt4_description = gpt4_description.strip("```json\n").strip("```")

    logging.info(gpt4_description)

    try:
        json_content = json.loads(gpt4_description)
        # Create a temporary JSON file
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
            temp_file.write(json.dumps(json_content).encode("utf-8"))
            temp_file_path = temp_file.name

        # Upload the JSON file to AWS S3
        with open(temp_file_path, "rb") as json_file:
            if aws_interface.upload_json(
                file_name=file_name + ".json", file_content=json_file.read()
            ):
                # Get the presigned URL for the uploaded JSON file
                # presigned_url = aws_repo.get_presigned_json_url(file_name=file_name+'json')
                os.unlink(temp_file_path)  # Delete the temporary file
                saved_json = database_interface.insert_one(
                    data={"filename": file_name, "username": "username"},
                    collection_name="json_files",
                )
                if "_id" in saved_json:
                    saved_json["_id"] = str(saved_json["_id"])
                return saved_json
            else:
                raise HTTPException(
                    status_code=500, detail="Failed to upload JSON to AWS S3"
                )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {e}")


@fhir_router.get("/get-all-json/{token}")
async def get_all_json(
    token: str,
    auth_interface: AuthInterface = Depends(auth_service),
    database_interface: DatabaseInterface = Depends(database_service),
):
    # Get all the JSON files uploaded by the specified user

    user = auth_interface.decode_access_token(token)
    all_json_files = database_interface.find_all_documents_from_field(
        "username", user["sub"], "json_files"
    )
    if all_json_files:
        return all_json_files
    else:
        raise HTTPException(
            status_code=404, detail="No JSON files found for the specified user"
        )


@fhir_router.post("/presigned-url")
async def get_presigned_url(
    file_name: FileName,
    aws_interface: AWSInterface = Depends(aws_service),
    token: str = Header(..., alias="Authorization"),
):
    logging.info(file_name)
    # Get the presigned URL for the specified file name
    presigned_url = aws_interface.get_presigned_json_url(
        file_name=file_name.fileName + ".json"
    )

    # Return the presigned URL
    if presigned_url:
        return {"presigned_url": presigned_url}
    else:
        raise HTTPException(
            status_code=404,
            detail="File not found or presigned URL generation failed",
        )
