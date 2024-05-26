from pymongo import MongoClient
from typing import Dict


class DatabaseRepository:
    def __init__(self):

        # Connect to the database
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["dophin"]

    def insert_single_document(self, data: str, collection_name: str):

        try:
            # Define the collection where the data will be stored
            collection = self.db[collection_name]

            # Insert the data into the collection
            collection.insert_one(data)

            # Return the data that was stored
            return data
        except Exception as e:
            return None

    def find_all(self, field: str, field_value: str, collection_name: str):

        # Create an empty list to store the data that will be found
        all_documents = []
        try:

            # Define the collection where the data will be stored
            collection = self.db[collection_name]

            # Find all the data that matches the username
            data = collection.find({field: field_value})

            for item in data:
                item["_id"] = str(item["_id"])
                all_documents.append(item)

            # Return the data that was found
            return all_documents
        except Exception as e:
            return None

    def check_if_file_belongs_to_user(self, username: str, pdf_name: str):
        try:

            # Define the collection where the data will be stored
            collection = self.db["pdfs"]

            # Find the data that matches the username and pdf name
            pdf_data = collection.find_one({"username": username, "pdf_name": pdf_name})

            if pdf_data is not None:
                return True
            else:
                return False

        except Exception as e:
            return False
        
    def find_single_document(self, field: str, field_value: str, collection_name: str):
        try:

            # Define the collection where the data will be stored
            collection = self.db[collection_name]

            # Find the data that matches the username
            result = collection.find_one({field: field_value})

            if result is  None:
                return None
            result["_id"] = str(result["_id"])

            # Return the data that was found
            return result
        except Exception as e:
            return None

    def delete_one(self, field: str, field_value: str, collection_name: str):
        try:
            # Define the collection where the data will be stored
            collection = self.db[collection_name]

            # Delete the data that matches the username
            a=collection.delete_one({field: field_value})
           
            # Return the data that was found
            return True
        except Exception as e:
            return False
        
    def append_entity_to_array(self, field: str, field_value: str, array_field: str, data: Dict[str, int], collection_name: str):
        try:
            # Define the collection where the data will be stored
            collection = self.db[collection_name]

            # Append the data to the array
            collection.update_one({field: field_value}, {"$push": {array_field: data}})
            return True
        except Exception as e:
            return False
