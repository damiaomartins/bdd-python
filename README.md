# bdd-python
A simple Flask application used for demonstration of the BDD testing features

## Running the application
Install dependencies: 

`pip install -r src/main/requirements.txt`

Export the path to app:

`export FLASK_APP="src/main/app.py"` 

Run flask:

`python -m flask run`

## Running the tests
Install test dependencies:

`pip install -r src/tests/requirements.txt`

Run pytest:

`python -m pytest`

## Running the BDD tests
Install test dependencies:

`pip install -r src/tests-bdd/requirements.txt`

Run behave:

`python -m behave`