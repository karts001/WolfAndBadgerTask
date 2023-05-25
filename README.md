# WolfAndBadgerTask
Flask website, which uses github OAuth, where the user can update personal information through a html form

Steps to run:

1. Clone the code
2. Create the virtual env using: "virtualenv .venv --python=python3.9"
3. Activate the environment using ". venv/bin/activate" in project root
4. Install the project requirements using pip install -r requirements.txt
5. Create secrets.env file in the flask_app directory

To run tests you can either run in an IDE like Pycharm or set Python path to the root of the project folder and run
"python -m unittest discover"