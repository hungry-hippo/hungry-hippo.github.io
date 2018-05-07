# encoding=utf-8
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired

from expecto_judicio.models import Laws


# TODO: https://flask-wtf.readthedocs.io/en/stable/quickstart.html#quickstart

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])


class CommentForm(FlaskForm):
    #username = StringField('Username: ', validators=[DataRequired()])
    text = StringField('Comment: ', validators=[DataRequired()])
    repliesto = HiddenField('Reply')


class CommentModifyForm(FlaskForm):
    #username = StringField('Username: ', validators=[DataRequired()])
    modifytext = StringField('Comment: ', validators=[DataRequired()])
    modifyid = HiddenField('Reply')


class DeleteForm(FlaskForm):
    id = HiddenField("id field")


class AddUserForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    usertype = SelectField('User Role: ', validators=None,
        choices=[('1', 'End User'), ('2', 'Legal Expert'), ('3', 'System Admin')],
    )


class LawsSearchForm(FlaskForm):
    secno = SelectField('Section No: ', validators=None)
    chapno = SelectField('Section No: ', validators=None)
    submitsec = SubmitField('Search')
    submitchap =SubmitField('Search')

    def __init__(self, min_entries=0, *args, **kwargs):
        super(LawsSearchForm, self).__init__(*args, **kwargs)
        self.secno.choices = [(a.sec, a.sec) for a in Laws.query.all()]
        self.chapno.choices = set([(b.chapter, b.chapter) for b in Laws.query.all()])


class LawsAddForm(FlaskForm):
    chapter = StringField('Chapter No: ', validators=[DataRequired()])
    sec = StringField('Section No: ', validators=[DataRequired()])
    legal = StringField('Legal Statement: ', validators=[DataRequired()])
    exp = StringField('Explanation: ', validators=[DataRequired()])
    add = SubmitField('Add')
