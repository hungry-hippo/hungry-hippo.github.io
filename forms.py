# encoding=utf-8
from flask_wtf import FlaskForm
from flask import flash

from wtforms import StringField, PasswordField, HiddenField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from expecto_judicio.models import Laws

from expecto_judicio.application import db

import re

# TODO: https://flask-wtf.readthedocs.io/en/stable/quickstart.html#quickstart


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

def username_type_check(form, field):
    if not re.match("^[a-zA-Z0-9_]*$", field.data):
        raise ValidationError('Invalid Characters Found. Username must contain only alphanumeric characters ')


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired(), Length(min=3,max=15, message="Username length must be between 3 and 15"), username_type_check])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit1 = SubmitField('Login')

class SignUpForm(FlaskForm):
    usernameS = StringField('Username: ', validators=[DataRequired(), Length(min=3,max=15, message="Username length must be between 3 and 15"), username_type_check])
    passwordS = PasswordField('Password: ', validators=[DataRequired(), Length(min=6,max=15, message="Password length must be between 6 and 15")])
    submit2 = SubmitField('Sign Up')

class CommentForm(FlaskForm):
    text = StringField('Comment: ', validators=[DataRequired(), Length(max=8000, message="Comment length must be less than 8000")])
    repliesto = HiddenField('Reply')


class CommentModifyForm(FlaskForm):
    modifytext = StringField('Comment: ', validators=[DataRequired(), Length(max=8000, message="Comment length must be less than 8000")])
    modifyid = HiddenField('Reply')
    commentmod = SubmitField('Modify')


class PostAddForm(FlaskForm):
    text = TextAreaField('Content: ',
                       validators=[DataRequired(), Length(max=8000, message="Comment length must be less than 8000")])
    heading = StringField('Heading: ',
                       validators=[DataRequired(), Length(max=500, message="Heading length must be less than 500")])


class DeleteForm(FlaskForm):
    id = HiddenField("id field")


class AddUserForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired(), Length(min=3,max=15, message="Username length must be between 3 and 15"), username_type_check])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6,max=15, message="Password length must be between 6 and 15")])
    usertype = SelectField('User Role: ', validators=None,
        choices=[('1', 'End User'), ('2', 'Legal Expert'), ('3', 'System Admin')],
    )
    adduser = SubmitField('Add')


class LawsSearchForm(FlaskForm):
    #secno = SelectField('Section No: ', validators=None)
    chapno = SelectField('Chapter No: ', validators=None)
    #submitsec = SubmitField('Search')
    submitchap =SubmitField('Search')

    def __init__(self, min_entries=0, *args, **kwargs):
        super(LawsSearchForm, self).__init__(*args, **kwargs)
        #self.secno.choices = [(a.sec, a.sec) for a in Laws.query.all()]
        query = db.session.query(Laws.chapter.distinct().label("chapter"))
        self.chapno.choices = [(b.chapter, b.chapter) for b in query.all()]


class LawsAddForm(FlaskForm):
    chapter = StringField('Chapter No: ', validators=[DataRequired(), Length(max=200, message="Chapter length cannot be greater than 200")])
    sec = StringField('Section No: ', validators=[DataRequired(), Length(max=200, message="Section length cannot be greater than 200")])
    legal = TextAreaField('Legal Statement: ', validators=[DataRequired(), Length(max=8000, message="Legal Statement length cannot be greater than 8000")])
    exp = TextAreaField('Explanation: ', validators=[DataRequired(), Length(max=8000, message="Explanation length cannot be greater than 8000")])
    add = SubmitField('Add')


class LawsModifyForm(FlaskForm):
    chapter = StringField('Chapter No: ', validators=[DataRequired(), Length(max=200, message="Chapter length cannot be greater than 200")])
    sec = StringField('Section No: ', validators=[DataRequired(), Length(max=200, message="Section length cannot be greater than 200")])
    legal = TextAreaField('Legal Statement: ', validators=[DataRequired(), Length(max=8000, message="Legal Statement length cannot be greater than 8000")])
    exp = TextAreaField('Explanation: ', validators=[DataRequired(), Length(max=8000, message="Explanation length cannot be greater than 8000")])
    modify = SubmitField('Modify')
    modifyid = HiddenField('ModifyID')