# import os
#
# from dotenv import load_dotenv
# load_dotenv()
#
#
# class Config:
#     DEBUG = False
#     DEVELOPMENT = False
#     SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
#     FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI")
#
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#     DEVELOPMENT = True
