## About the application

Backend repository for the mobile application server which aims at making the health of the users better leveraging the use of AI.


## How to run the code

- First pull the repository. `git clone https://github.com/asifrahaman13/sniffle_backend.git`

- Go to the root directory. `cd sniffle_backend`

- create a virtual environment. `virtualenv .venv`

- Now install the dependencies. `pip install -r requirements.txt`

- Now rename the .env.example. `mv .env.example .env`. 

- Give the proper configuration by giving the API keys. For example set the open ai key, mapbox api key etc.

- Next you need to run the application using the following script: `python3  src/index.py`

## PORT

To connect to the server hit the link `http://localhost:8000`