import os

from flask import url_for
from flask_dance.contrib.github import github, make_github_blueprint
from werkzeug.utils import redirect

auth = make_github_blueprint(
    client_id=os.environ.get("FLASK_CLIENT_ID"),
    client_secret=os.environ.get("FLASK_CLIENT_SECRET"),
)


@auth.route("/")
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))

    else:
        return redirect(url_for("views.update_info"))
