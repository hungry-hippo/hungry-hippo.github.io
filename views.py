# encoding=utf-8
from flask import render_template, redirect, url_for
from flask.views import View

from flask_login import login_required, login_user, logout_user, current_user

from expecto_judicio.decorators import legal_expert_required, system_admin_or_legal_expert_required, system_admin_required
from expecto_judicio.forms import *

from expecto_judicio.models import *

from sqlalc import Example
#from flask import Flask,render_template
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


class SamplePageRoot(View):
    endpoint = 'sample_page_root'

    def dispatch_request(self):
        return 'Root Page'


class SamplePageA(View):
    endpoint = 'sample_page_a'

    def dispatch_request(self):
        form = LoginForm()
        signupform = LoginForm()
        #print '1'
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                auth = user.validate_password(form.password.data)
                if auth:
                    login_user(user)
                    return redirect(url_for('sample_page_b'))
                else:
                    return redirect(url_for('sample_page_root'))
        if signupform.validate_on_submit():
            newuser = User(signupform.username.data,signupform.password.data, 1)
            newuser.add_user()
        #print '3'
        return render_template('form.html', form=form, signform=signupform, user=current_user)

        #return 'Everyone can view this page'


class SamplePageB(View):
    endpoint = 'sample_page_b'
    decorators = [login_required]

    def dispatch_request(self):
        data = Comments.query.all()
        form = CommentForm()
        delform = DeleteForm()
        if form.validate_on_submit():
            comment = Comments(current_user.username, form.text.data, current_user.usertype)
            comment.add_comment()
            return redirect(url_for('sample_page_b'))
        if delform.id.data:
            deluser = Comments.query.filter_by(id=delform.id.data).first()
            deluser.delete_comment()
            return redirect(url_for('sample_page_b'))
        return render_template('forum.html', form=form, delform=delform, data=data, user=current_user)


#add users
class SamplePageC(View):
    endpoint = 'sample_page_c'
    decorators = [login_required, system_admin_required]

    def dispatch_request(self):
        data = User.query.all()
        delform = DeleteForm()
        form = AddUserForm() #used to modify users. Will have same fields
        if delform.id.data:
            deluser = User.query.filter_by(id=delform.id.data).first()
            deluser.delete_user()
            return redirect(url_for('sample_page_c'))
        if form.validate_on_submit():
            #print 1
            newuser = User(form.username.data, form.password.data,int(form.usertype.data))
            #print newuser
            newuser.add_user()
            return redirect(url_for('sample_page_c'))
        return render_template('manage_users.html', delform=delform, form=form, data=data, currentuser=current_user)

#??
class SamplePageD(View):
    endpoint = 'sample_page_d'
    #decorators = [login_required, legal_expert_required]

    def dispatch_request(self, name):
        example = Laws.query.all()
        s1 = []
        flag = 0
        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = set(stopwords.words('english'))
        name = name.lower()
        query = tokenizer.tokenize(name)
        filtered_query = [w for w in query if not w in stop_words]
        for ex in example:
            words = tokenizer.tokenize(ex.legal)
            words1 = []
            for word in words:
                if word[0] == '"':
                    l = len(word)
                    word = word[1:l - 1]
                words1.append(word.lower())
            for nm in filtered_query:
                if nm in words1:
                    temp = []
                    for i in [ex.sec, ex.legal]:
                        temp.append(i)
                    s1.append(tuple(temp))
                    flag = 1
                    break
        if flag == 1:
            return render_template("format.html", name=s1)
        else:
            return '<html><body><p>Sorry no results matched your query</p></body></html>'

#manipulate database
class SamplePageE(View):
    endpoint = 'sample_page_e'
    decorators = [login_required, system_admin_or_legal_expert_required]

    def dispatch_request(self):
        return 'You need to be logged in and be either a legal expert or system admin to view this page'


class Logout(View):
    endpoint = 'logout'
    decorators = [login_required]

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('sample_page_a'))


