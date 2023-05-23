# WolfAndBadgerTask
Flask website, which uses github OAuth, where the user can update personal information through a html form

Note:
test.env, development.env, and requirements.txt files have been included to make setting up and running the app and the
test suite simpler.

To protect my keys and secrets I have not included them in this repository, so in order to run the app you will need to
create secrets.env file in the flask_app directory.

To run tests you can either run in an IDE like Pycharm or set Python path to the root of the project folder and run
"python -m unittest discover"