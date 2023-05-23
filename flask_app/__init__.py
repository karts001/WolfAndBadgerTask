import os
import pathlib

from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap

from flask_app.extensions import db


def create_app(env):
    """create and configure the app"""
    # check which env we are working in
    base_file_path = pathlib.Path(__file__).parent.resolve()
    print(base_file_path)
    if env == "local":
        path = os.path.join(base_file_path, "development.env")
    elif env == "test":
        path = os.path.join(base_file_path, "test.env")

    secret_path = os.path.join(base_file_path, "secrets.env")

    load_dotenv(path)
    load_dotenv(secret_path)
    app = Flask(__name__)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    Bootstrap(app)

    app.config.from_prefixed_env()

    from flask_app.src.routes.views import views

    app.register_blueprint(views, url_prefix="/authorized")

    from flask_app.src.routes.auth import auth

    app.register_blueprint(auth, url_prefix="/")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
