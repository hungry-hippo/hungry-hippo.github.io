# encoding=utf-8
from hashlib import sha512

from flask_login import UserMixin
from flask import flash
from expecto_judicio.application import db, bcrypt_

from sqlalchemy import exc


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
        try:
            db.session.commit()
        except exc.IntegrityError as err:
            print(err)
            db.session.rollback()

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
    heading = db.Column(db.String(140))

    def __init__(self, username, text, usertype, replyto, heading=None):
        self.username = username
        self.text = text
        self.usertype = usertype
        self.replyto = replyto
        self.heading = heading

    def add_comment(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError as err:
            print(err)
            db.session.rollback()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    def modify_comment(self, newdata):
        self.text = newdata
        db.session.commit()


class Laws(db.Model):
    __tablename__='laws'
    id = db.Column('id', db.Integer, primary_key=True)
    chapter=db.Column('Chapter',db.String(200))
    sec=db.Column('Section',db.String(200))
    legal=db.Column('Legal Statement',db.String(8000))
    exp=db.Column('Explanation',db.String(8000))
    addedby = db.Column('Added By', db.String(80))
    modifiedby = db.Column('Modified By', db.String(80))

    def __init__(self, chapter, sec, legal, exp, addedby):
        self.chapter = chapter
        self.sec = sec
        self.legal = legal
        self.exp = exp
        self.addedby = addedby
        self.modifiedby = '-'

    def add_law(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError as err:
            print(err)
            db.session.rollback()

    def delete_law(self):
        db.session.delete(self)
        db.session.commit()

    def modify_law(self, chapter,sec,legal,exp,user):
        self.chapter = chapter
        self.sec = sec
        self.legal = legal
        self.exp = exp
        self.modifiedby = user
        db.session.commit()