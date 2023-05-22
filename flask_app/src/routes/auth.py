from flask import url_for
from flask_dance.contrib.github import make_github_blueprint, github
from werkzeug.utils import redirect


"""move into a config file"""
auth = make_github_blueprint(client_id="77ae2a7d12b314d52eeb",
                             client_secret="28134967312b14a2267c4e3a81268dbce9137a13")


@auth.route("/")
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))

    else:
        return redirect(url_for('views.update_info'))
