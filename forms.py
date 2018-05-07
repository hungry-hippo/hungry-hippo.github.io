# encoding=utf-8
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, HiddenField, SelectField
from wtforms.validators import DataRequired


# TODO: https://flask-wtf.readthedocs.io/en/stable/quickstart.html#quickstart

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])


class CommentForm(FlaskForm):
    #username = StringField('Username: ', validators=[DataRequired()])
    text = StringField('Comment: ', validators=[DataRequired()])


class DeleteForm(FlaskForm):
    id = HiddenField("id field")


class AddUserForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    usertype = SelectField('User Role: ', validators=None,
        choices=[('1', 'End User'), ('2', 'Legal Expert'), ('3', 'System Admin')],
    )

