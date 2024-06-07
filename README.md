## About the application

Backend repository for the mobile application server which aims at making the health of the users better leveraging the use of AI.

# Tech stacks used:
- **FastAPI**: A high perfomant python based framework for creating backend server. 📈
- **Mongo db database**: A NoSQL database. Preferred this over the SQL database due to performance and highly unstructured data required. 📊
- **openai, langchain, Deepgram SDKs and other libraries**: They are libraries to deal with LLMs, Voice and other AI based works. 🤖
- **AWS**: Use the S3 service of AWS to store FHIR files. ☁️

## Deploy:

The service is deployed on render.com. https://sniffle-backend.onrender.com/

Find the front end repository corresponding to this repo here: https://github.com/asifrahaman13/sniffle_mobile.git

## How to run the code

- First pull the repository. `git clone https://github.com/asifrahaman13/sniffle_backend.git`

- Go to the root directory. `cd sniffle_backend`

- create a virtual environment. `virtualenv .venv`

- Now install the dependencies. `pip install -r requirements.txt`

- Now rename the .env.example. `mv .env.example .env`. 

- Give the proper configuration by giving the API keys. For example set the open ai key, mapbox api key etc. Also set the configuration data in the config.yaml file. If you are using redis server instead of local redis environment please change the redis.conf file.

- Next you need to run the application using the following script: `uvicorn src.main:app --reload`

## Run with docker

In case you face any issue with the installtion and set up, you can run using docker.

`docker build -t dolphin:lastest `

Next you can run the application:

`docker run -p 8000:8000 dolphin:latest`

## PORT

To connect to the server hit the link `http://localhost:8000`