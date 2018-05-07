# encoding=utf-8
from hashlib import sha512

from flask_login import UserMixin

from expecto_judicio.application import db, bcrypt_

from expecto_judicio.user_type import Role


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True)
    # TODO: add some kind of user type so you can differ between system admins and legal experts
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column('password', db.String(length=60), nullable=False)
    usertype = db.Column(db.INT, nullable=False)

    def __init__(self, uname, pword, utype):
        self.username = uname
        self.password = self.hash_password(pword)
        self.usertype = utype

    def validate_password(self, password):
        return bcrypt_.check_password_hash(self.password, sha512(str(password)).hexdigest())

    @staticmethod
    def hash_password(password):
        return bcrypt_.generate_password_hash(sha512(str(password)).hexdigest())

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def modify_user(self, newdata):
        db.session.delete(self)
        db.session.add(newdata)
        db.session.commit()


class Comments(db.Model, UserMixin):

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(8000), nullable=False)
    usertype = db.Column(db.INT, nullable=False)
    replyto = db.Column(db.INT, nullable=False)

    def __init__(self, username, text, usertype, replyto):
        self.username = username
        self.text = text
        self.usertype = usertype
        self.replyto = replyto

    def add_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    def modify_comment(self, newdata):
        self.text = newdata
        db.session.commit()


class Laws(db.Model):
    __tablename__='laws'
    chapter=db.Column('Chapter No',db.VARCHAR)
    sec=db.Column('Section No.',db.VARCHAR,primary_key=True)
    legal=db.Column('Legal Statement as mentioned in the IPC',db.VARCHAR)
    exp=db.Column('Explaination/Illustration of the Legal Statement',db.VARCHAR)

    def __init__(self, chapter, sec, legal, exp):
        self.chapter = chapter
        self.sec = sec
        self.legal = legal
        self.exp = exp

    def add_law(self):
        db.session.add(self)
        db.session.commit()

    def delete_law(self):
        db.session.delete(self)
        db.session.commit()

    def modify_law(self, newdata):
        db.session.delete(self)
        db.session.add(newdata)
        db.session.commit()