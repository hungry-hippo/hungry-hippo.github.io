# encoding=utf-8
from flask_wtf import FlaskForm
from flask import flash

from wtforms import StringField, PasswordField, HiddenField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from expecto_judicio.models import Laws

from expecto_judicio.application import db

import re


# error handling code in case if any error occurs while handling the form
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


# function to check the user_name type entered by the user
def username_type_check(form, field):
    if not re.match("^[a-zA-Z0-9_]*$", field.data):

        # if it does not match raise a validation error, informing the user about his mistake
        raise ValidationError('Invalid Characters Found. Username must contain only alphanumeric characters ')


# function to handle the login into the site.
class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired("Username Required"), Length(min=3,max=15,
                                            message="Username length must be between 3 and 15"), username_type_check])
    password = PasswordField('Password: ', validators=[DataRequired("Password Required")])
    submit1 = SubmitField('Login')


# class to implement the sign up of a user
class SignUpForm(FlaskForm):
    usernameS = StringField('Username: ', validators=[DataRequired("Username Required"), Length(min=3,max=15,
                                            message="Username length must be between 3 and 15"), username_type_check])
    passwordS = PasswordField('Password: ', validators=[DataRequired("Password Required"), Length(min=6,max=15,
                                            message="Password length must be between 6 and 15")])
    submit2 = SubmitField('Sign Up')


# class to implement commenting by a logged in user
class CommentForm(FlaskForm):
    text = StringField('Comment: ', validators=[DataRequired("Text Required"), Length(max=8000,
                                                                    message="Comment length must be less than 8000")])
    repliesto = HiddenField('Reply')


# class called when required ro modify an already existing comment, posted by a user.
class CommentModifyForm(FlaskForm):
    modifytext = StringField('Comment: ', validators=[DataRequired("Text Required"), Length(max=8000,
                                                                    message="Comment length must be less than 8000")])
    modifyid = HiddenField('Reply')
    commentmod = SubmitField('Modify')


# class to implement the fucntionality of adding a post in the forum
class PostAddForm(FlaskForm):
    text = TextAreaField('Content: ',
                       validators=[DataRequired("Text Required"), Length(max=8000,
                                                                    message="Comment length must be less than 8000")])
    heading = StringField('Heading: ',
                       validators=[DataRequired("Heading Required"), Length(max=500,
                                                                    message="Heading length must be less than 500")])


class DeleteForm(FlaskForm):
    id = HiddenField("id field")


# class called to add a particular user in the forum
class AddUserForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired("Username Required"), Length(min=3,max=15,
                                            message="Username length must be between 3 and 15"), username_type_check])
    password = PasswordField('Password: ', validators=[DataRequired("Password Required"), Length(min=6,max=15,
                                            message="Password length must be between 6 and 15")])
    usertype = SelectField('User Role: ', validators=None,
        choices=[('1', 'End User'), ('2', 'Legal Expert'), ('3', 'System Admin')],
    )
    adduser = SubmitField('Add')


# class that would be called when the legal experts would want to search a particular law in the database
class LawsSearchForm(FlaskForm):
    chapno = SelectField('Chapter No: ', validators=None)
    submitchap =SubmitField('Search')

    def __init__(self, min_entries=0, *args, **kwargs):
        super(LawsSearchForm, self).__init__(*args, **kwargs)
        query = db.session.query(Laws.chapter.distinct().label("chapter"))
        self.chapno.choices = [(b.chapter, b.chapter) for b in query.all()]


# class used to add any new law to the existing database
class LawsAddForm(FlaskForm):
    chapter = StringField('Chapter No: ', validators=[DataRequired("Chapter Name Required"),
                                        Length(max=200, message="Chapter length cannot be greater than 200")])
    sec = StringField('Section No: ', validators=[DataRequired("Section Number Required"),
                                        Length(max=200, message="Section length cannot be greater than 200")])
    legal = TextAreaField('Legal Statement: ', validators=[DataRequired("Statement Required"),
                                        Length(max=200, message="Legal Statement length cannot be greater than 8000")])
    exp = TextAreaField('Explanation: ', validators=[DataRequired("Explanation Required"),
                                        Length(max=200, message="Explanation length cannot be greater than 8000")])
    add = SubmitField('Add')


# this class will be called when the legal expert wants to modify an existing law in the database.
class LawsModifyForm(FlaskForm):
    chapter = StringField('Chapter No: ', validators=[DataRequired("Chapter Name Required"),
                                        Length(max=200, message="Chapter length cannot be greater than 200")])
    sec = StringField('Section No: ', validators=[DataRequired("Section Number Required"),
                                        Length(max=200, message="Section length cannot be greater than 200")])
    legal = TextAreaField('Legal Statement: ', validators=[DataRequired("Statement Required"),
                                        Length(max=200, message="Legal Statement length cannot be greater than 8000")])
    exp = TextAreaField('Explanation: ', validators=[DataRequired("Explanation Required"),
                                        Length(max=200,  message="Explanation length cannot be greater than 8000")])
    modify = SubmitField('Modify')

    # the id field has been hidden as it is the primary key of the table and it would be auto-incremented.
    modifyid = HiddenField('ModifyID')