# encoding=utf-8
from hashlib import sha512

from flask_login import UserMixin
from expecto_judicio.application import db, bcrypt_

from flask import flash, jsonify

from sqlalchemy import exc

# this class basically handles all the registered users
class User(db.Model, UserMixin):

    # all the informatiion about the user gets stored in the 'user' table
    __tablename__ = 'user'

    #id,username,password,usertype are all the attributes of the 'user' table
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column('password', db.String(length=60), nullable=False)
    usertype = db.Column(db.INT, nullable=False)

    # constructor to initialise the object
    def __init__(self, uname, pword, utype):
        self.username = uname
        self.password = self.hash_password(pword)
        self.usertype = utype
	
    def validate_password(self, password):
        return bcrypt_.check_password_hash(self.password, sha512(str(password)).hexdigest())

    @staticmethod
    def hash_password(password):
        return bcrypt_.generate_password_hash(sha512(str(password)).hexdigest())

    # called to add user
    def add_user(self):
        db.session.add(self)
        try:
            db.session.commit()
            return 0
        except exc.IntegrityError as err:
            db.session.rollback()
            return 2

    # called to delete a user from the 'user' table
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


# used to manage all the comments that are being added by the logged in users and legal experts
class Comments(db.Model, UserMixin):

    #below are the various fields of the table where the comments are being stored
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(8000), nullable=False)
    usertype = db.Column(db.INT, nullable=False)
    replyto = db.Column(db.INT, nullable=False)
    heading = db.Column(db.String(140))

    #constructor
    def __init__(self, username, text, usertype, replyto, heading=None):
        self.username = username
        self.text = text
        self.usertype = usertype
        self.replyto = replyto
        self.heading = heading

    # used to add comments
    def add_comment(self):
        db.session.add(self)
        try:
            db.session.commit()
            return 0
        except exc.IntegrityError as err:
            db.session.rollback()
            return 2

    #used to delete an existing comment
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    # used to modify a comment
    def modify_comment(self, newdata):
        self.text = newdata
        db.session.commit()


# class used to access the database 
class Laws(db.Model):
    __tablename__='laws'
    id = db.Column('id', db.Integer, primary_key=True)
    chapter=db.Column('Chapter',db.String(200))
    sec=db.Column('Section',db.String(200))
    legal=db.Column('Legal Statement',db.String(8000))
    exp=db.Column('Explanation',db.String(8000))
    addedby = db.Column('Added By', db.String(80))
    modifiedby = db.Column('Modified By', db.String(80))

    # constructor
    def __init__(self, chapter, sec, legal, exp, addedby):
        self.chapter = chapter
        self.sec = sec
        self.legal = legal
        self.exp = exp
        self.addedby = addedby
        self.modifiedby = '-'

    # function to add new law in the database
    def add_law(self):
        db.session.add(self)
        try:
            db.session.commit()
            return 0
        except exc.IntegrityError as err:
            db.session.rollback()
            return 2

    # function to delete existing law
    def delete_law(self):
        db.session.delete(self)
        db.session.commit()

    # function to modify existing law, maybe the chapter no., section no., etc
    def modify_law(self, chapter,sec,legal,exp,user):
        self.chapter = chapter
        self.sec = sec
        self.legal = legal
        self.exp = exp
        self.modifiedby = user
        db.session.commit()