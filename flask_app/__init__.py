import os
from dotenv import load_dotenv
from flask import Flask
from flask_app.extensions import db
from flask_bootstrap import Bootstrap


def create_app(env):
    """create and configure the app"""
    # check which env we are working in
    if env == 'local':
        path = r'C:\Users\shivi\Repos\WolfAndBadgerTask\flask_app\development.env'
    elif env == 'test':
        path = r'C:\Users\shivi\Repos\WolfAndBadgerTask\flask_app\test.env'

    load_dotenv(path)
    app = Flask(__name__)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
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
