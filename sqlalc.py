# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 20:57:07 2018

@author: Lenovo
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

_database_settings = {
    'host': 'localhost',
    'username': 'root',
    'password': '',
    'database': 'mydb'
}

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://{username}:{password}@{host}/{database}'.format(**_database_settings)
db=SQLAlchemy(app)

class Example(db.Model):
    __tablename__='laws'
    chapter=db.Column('Chapter No',db.VARCHAR)
    sec=db.Column('Section No.',db.VARCHAR,primary_key=True)
    legal=db.Column('Legal Statement as mentioned in the IPC',db.VARCHAR)
    exp=db.Column('Explaination/Illustration of the Legal Statement',db.VARCHAR)