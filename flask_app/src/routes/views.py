from flask import Blueprint, render_template, request, url_for
from flask_dance.contrib.github import github
from werkzeug.utils import redirect

from flask_app.extensions import db
from flask_app.src.forms.personal_info import PersonalInfoForm
from flask_app.src.models.personal_info import PersonalInfo

views = Blueprint("views", __name__)


@views.route("/update_info", methods=["GET", "POST"])
def update_info():
    """Route which contains the html form"""
    personal_info_form = PersonalInfoForm()
    github_name = get_user_info()
    # query the database for the current user using the github username
    user = PersonalInfo.query.filter_by(github_user_name=github_name).first()

    if personal_info_form.validate_on_submit() and "submit" in request.form:
        if user is not None:
            # if the user exists in the DB, update the record
            user.first_name = personal_info_form.first_name.data
            user.last_name = personal_info_form.last_name.data
            user.age = personal_info_form.age.data
            user.email = personal_info_form.email.data
            user.phone_number = personal_info_form.phone_number.data
            user.address = personal_info_form.address.data
            user.post_code = personal_info_form.post_code.data
        else:
            # create a new record if the user does not exist
            user = PersonalInfo(
                github_user_name=github_name,
                first_name=personal_info_form.first_name.data,
                last_name=personal_info_form.last_name.data,
                age=personal_info_form.age.data,
                email=personal_info_form.email.data,
                phone_number=personal_info_form.phone_number.data,
                address=personal_info_form.address.data,
                post_code=personal_info_form.post_code.data,
            )

            db.session.add(user)

        db.session.commit()

        return redirect(url_for("views.info_updated"))

    elif request.method == "GET":
        # populate the form with data from the database if it exists
        if user is not None:
            personal_info_form.first_name.data = user.first_name
            personal_info_form.last_name.data = user.last_name
            personal_info_form.age.data = user.age
            personal_info_form.email.data = user.email
            personal_info_form.phone_number.data = user.phone_number
            personal_info_form.address.data = user.address
            personal_info_form.post_code.data = user.post_code

        return render_template(
            "index.html",
            form=personal_info_form,
            personal_info=user,
            github_user=github_name,
        )

    elif request.method == "POST" and "delete_button" in request.form:
        return redirect(url_for("views.delete_record", github_user=github_name))

    else:
        # Render an empty form
        return render_template(
            "index.html",
            form=personal_info_form,
            personal_info=user,
            github_user=github_name,
        )


@views.route("/info_updated", methods=["GET"])
def info_updated():
    """Route for when the user's info has been successfully updated"""
    return render_template("info_updated.html")


@views.route("/delete_record/<github_user>", methods=["GET", "POST"])
def delete_record(github_user):
    """Route for when a user's record is deleted from the database"""
    PersonalInfo.query.filter_by(github_user_name=github_user).delete()
    db.session.commit()

    return render_template("user_deleted.html", github_user=github_user)


def get_user_info():
    """Gets users info from GitHub OAuth, also allows GitHub OAuth to be mocked in the unit tests"""
    account_info = github.get("/user")
    account_info_json = account_info.json()
    github_name = account_info_json["login"]

    return github_name
