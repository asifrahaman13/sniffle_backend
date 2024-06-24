## Contribution guidelines  


- First pull the repository. `git clone https://github.com/asifrahaman13/sniffle_backend.git`

- Go to the root directory. `cd sniffle_backend`

- create a virtual environment. `virtualenv .venv`. You need to actiavate the virtual environment too. `source .venv/bin/activate`

- Now install the dependencies. `pip install -r requirements.txt`

- Now rename the .env.example. `mv .env.example .env`.  Give the proper configuration by giving the API keys. For example set the open ai key, deepgram api key etc. Also set the configuration data in the config.yaml file. If you are using redis server instead of local redis environment please change the redis.conf file.

- Next you need to run the application using the following script: `uvicorn src.main:app --reload`

## Install precommit hooks.

 `pre-commit install`

## Run with docker

Best way of utilizing the docker is through the docker compose file.

`docker compose up -d`

In case you face any issue with the installtion and set up, you can run using docker.

`docker build -t dolphin:lastest .`

Next you can run the application:

`docker run -p 8000:8000 dolphin:latest`

## PORT

To connect to the server hit the link `http://localhost:8000`
