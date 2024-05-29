## About the application

First pull the repository. `git clone https://github.com/asifrahaman13/sniffle_backend.git`

Go to the root directory. `cd DeepgramStream`

create a virtual environment. `virtualenv .venv`

Now install the dependencies. `pip install -r requirements.txt`

Now rename the .env.example. `mv .env.example .env`. 

Give the proper configuration by giving the API keys. For example set the open ai key, mapbox api key etc.

Next you need to run the application using the following script: `python3  src/index.py`

To connect to the server hit the link `http://localhost:8000`