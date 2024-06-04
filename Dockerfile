# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the Python script
CMD ["uvicorn", "src.main:app", "--reload", "--port",  "${PORT}"]
