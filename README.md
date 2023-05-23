# WolfAndBadgerTask
Flask website, which uses github OAuth, where the user can update personal information through a html form

Running and using the app:
- To run the app cd into the flask_app directory and use the flask run command.
- Then visit the following url: http://127.0.0.1:5000/
- You will be redirected to the github authentication page
- Once logged in you can fill out the form and use the submit button to "Submit" the data to the database or click the
"Delete Record" button to remove your user from the database.

Note:
test.env, development.env, and requirements.txt files have been included to make setting up and running the app and the
test suite simpler.

To protect my keys and secrets I have not included them in this repository, so in order to run the app you will need to
create secrets.env file in the flask_app directory.

To run tests you can either run in an IDE like Pycharm or set Python path to the root of the project folder and run
"python -m unittest discover"

