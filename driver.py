# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 21:51:42 2018

@author: Lenovo
"""

from sqlalc import Example
from flask import Flask,render_template
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
app= Flask(__name__)

example=Example.query.all()
@app.route('/')
def index():
    return "Hey ya!"


@app.route('/<name>')
def action(name):
    s1=[]
    flag=0
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    name=name.lower()
    query=tokenizer.tokenize(name)
    filtered_query=[]
    filtered_query = [w for w in query if not w in stop_words]
    for ex in example:
        words=tokenizer.tokenize(ex.legal)
        words1=[]
        for word in words:
            if word[0]=='"':
                l=len(word)
                word=word[1:l-1]
            words1.append(word.lower())
        for nm in filtered_query:
            temp=[]
            if nm in words1:
                temp=[]
                for i in [ex.sec,ex.legal]:
                    temp.append(i)
                s1.append(tuple(temp))
                flag=1
                break
    if flag==1:
        return render_template("format.html",name=s1)
    else:
        return '<html><body><p>Sorry no results matched your query</p></body></html>'

if(__name__ == '__main__'):
    app.run(debug=True)
            