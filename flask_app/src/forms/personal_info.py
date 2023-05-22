from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email, NumberRange, Length


class PersonalInfoForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    age = IntegerField(label='Age', validators=[DataRequired(), NumberRange(min=0, max=100)])
    email = EmailField(label='Email', validators=[Email(message="Please enter a valid email!")])
    phone_number = StringField(label='Phone Number', validators=[DataRequired(), Length(12, 16)])
    address = StringField(label='Address', validators=[DataRequired()])
    post_code = StringField(label='Post Code', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
