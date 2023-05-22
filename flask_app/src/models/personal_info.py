from flask_app.extensions import db


class PersonalInfo(db.Model):
    __tablename__ = "personal_info"
    id = db.Column(db.Integer, primary_key=True)
    github_user_name = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(16))
    address = db.Column(db.String(200))
    post_code = db.Column(db.String(50))
