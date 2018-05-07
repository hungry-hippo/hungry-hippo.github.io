# encoding=utf-8
from flask import render_template, redirect, url_for, request
from flask.views import View

from flask_login import login_required, login_user, logout_user, current_user

from werkzeug.exceptions import NotFound

from expecto_judicio.forms import *
from expecto_judicio.decorators import*

from expecto_judicio.models import *

from expecto_judicio.models import Laws
#from flask import Flask,render_template
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import feedparser
feedparser._HTMLSanitizer.acceptable_elements.update(['iframe'])

import re
#loginform = LoginForm()

#class TrackCases(View):
#    endpoint = 'track_cases'
#
#    def dispatch_request(self):
#        feeddata=feedparser.parse('http://www.livelaw.in/news-updates/feed/')
#        #print feeddata
#        return render_template('tracksupremecourt.html', feeddata=feeddata, id=id)


class TrackCaseResult(View):
    endpoint = 'track_case_result'

    def dispatch_request(self, id):
        #print id
        feeddata=feedparser.parse('http://www.livelaw.in/news-updates/feed/')
        for data in feeddata.entries:
            numericid = ''.join(c for c in data.id if c.isdigit())
            #print data.description
            match = re.search(r'<img.*?>(.*?)<p', data.description)
            data.description = data.description.replace(match.group(1),'')
            #print data.description
            #if match:
            #    print match.group(1)
            #print numericid
            #print id
            if numericid == id:
                #print data
                return render_template('tracksupremecourtresult.html', feeddata=data, user=current_user)

        return '<h2>No Results Found</h2>'


class HomePage(View):
    endpoint = 'home_page'

    def dispatch_request(self):
        loginform = LoginForm()
        signupform = SignUpForm()
        incorrect = ''
        global flag
        flag=0
        feeddata = feedparser.parse('http://www.livelaw.in/news-updates/feed/')

        if loginform.validate_on_submit():
            user = User.query.filter_by(username=loginform.username.data).first()
            if user:
                auth = user.validate_password(loginform.password.data)
                if auth:
                    login_user(user)
                    flag=0
                    return redirect(url_for('home_page'))
                else:
                    incorrect = 'Invalid Password'
                    flag=1
                    #flash(u"Invalid Password")
                    #return render_template('form.html', loginform=loginform, signform=signupform, user=current_user,
                    #                      incorrect=incorrect, feeddata=feeddata, flag=flag)
            else:
                incorrect='Invalid Username'
                flag=1
                #return render_template('form.html', loginform=loginform, signform=signupform, user=current_user,
                #                       incorrect=incorrect, feeddata=feeddata, flag=flag)
        elif loginform.submit1.data:
            flash_errors(loginform)
            flag=1


        if signupform.validate_on_submit():
            newuser = User(signupform.usernameS.data,signupform.passwordS.data, 1)
            newuser.add_user()
            return redirect(url_for('home_page'))
        elif signupform.submit2.data:
            flash_errors(signupform)
            flag=2

        return render_template('form.html', loginform=loginform, signform=signupform, user=current_user, incorrect=incorrect,
                               feeddata=feeddata, flag=flag)

        #return 'Everyone can view this page'

#add users
class ManageUsers(View):
    endpoint = 'manage_users'
    decorators = [login_required, system_admin_required]

    def dispatch_request(self):
        loginform = LoginForm()
        data = User.query.all()
        delform = DeleteForm()
        form = AddUserForm() #used to modify users. Will have same fields
        if delform.id.data:
            deluser = User.query.filter_by(id=delform.id.data).first()
            deluser.delete_user()
            return redirect(url_for('manage_users'))
        if form.validate_on_submit():
            #print 1
            newuser = User(form.username.data, form.password.data,int(form.usertype.data))
            #print newuser
            newuser.add_user()
            return redirect(url_for('manage_users'))
        return render_template('manage_users.html', delform=delform, form=form, data=data, loginform=loginform,
                               user=current_user)


#SearchResults
class SearchResults(View):
    endpoint = 'search_results'
    #decorators = [login_required, legal_expert_required]

    def dispatch_request(self, name):
        loginform = LoginForm()
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
                    for i in [ex.sec, ex.legal, ex.exp]:
                        temp.append(i)
                    s1.append(tuple(temp))
                    flag = 1
                    break
        return render_template("format.html", name=s1, loginform=loginform, user=current_user, flag=flag)

#manipulate database
class LegalDatabaseAccess(View):
    endpoint = 'legal_database_access'
    decorators = [login_required, legal_expert_required]

    def dispatch_request(self):
        loginform = LoginForm()
        form = LawsSearchForm()
        delform = DeleteForm()
        addform = LawsAddForm()
        modform = LawsModifyForm()
        laws=None
        if form.validate_on_submit():
            #print 1
            if form.submitchap.data:
                #print("laws")
                laws = Laws.query.filter_by(chapter=form.chapno.data).all()
            #if form.submitsec.data:
            #    laws = Laws.query.filter_by(sec=form.secno.data).all()
            redirect(url_for('legal_database_access'))
        #print delform.id.data
        if delform.id.data:
            #print 2
            deluser = Laws.query.filter_by(id=delform.id.data).first()
            deluser.delete_law()
            #print deluser
            return redirect(url_for('legal_database_access'))

        if addform.validate_on_submit() and addform.add.data:
            #print addform.validate_on_submit()
            #print addform.validate()
            #print addform.add.data
            newlaw = Laws(addform.chapter.data, addform.sec.data, addform.legal.data, addform.exp.data, current_user.username)
            newlaw.add_law()
            return redirect(url_for('legal_database_access'))

        if modform.validate_on_submit():
            #print 4
            #print modform.validate_on_submit()
            id = modform.modifyid.data
            modified = Laws.query.filter_by(id=id).first()
            modified.modify_law(modform.chapter.data,modform.sec.data,modform.legal.data,modform.exp.data,current_user.username)
            return redirect(url_for('legal_database_access'))

        return render_template('legal_database_page.html', form=form, laws=laws, delform=delform, addform=addform,
                               loginform=loginform, user=current_user, modform=modform)


class Logout(View):
    endpoint = 'logout'
    decorators = [login_required]

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('home_page'))


class ForumTemp1(View):

    endpoint = 'forum_temp1'
    #decorators = [login_required]

    def dispatch_request(self):
        loginform = LoginForm()
        data = Comments.query.all()
        form = PostAddForm()
        delform = DeleteForm()
        #modifyform = CommentModifyForm()
        if form.validate_on_submit():
            comment = Comments(current_user.username, form.text.data, current_user.usertype, 0, form.heading.data)
            # print comment.text
            comment.add_comment()
            return redirect(url_for('forum_temp1'))

        #if modifyform.validate_on_submit():
        #    data = Comments.query.filter_by(id=modifyform.modifyid.data).first()
        #    data.modify_comment(modifyform.modifytext.data)
        #    return redirect(url_for('user_forum'))

        if delform.id.data:
            deluser = Comments.query.filter_by(id=delform.id.data).first()
            deluser.delete_comment()
            replies = Comments.query.filter_by(replyto=delform.id.data).all()
            for reply in replies:
                reply.delete_comment()
            return redirect(url_for('forum_temp1'))
        return render_template('forumtemp1.html', form=form, delform=delform, data=data,
                               loginform=loginform, user=current_user)


class ForumTemp2(View):
    endpoint = 'forum_temp2'
    #decorators = [login_required]

    def dispatch_request(self, id):
        loginform = LoginForm()
        heading = Comments.query.filter_by(id=id).first()
        if not heading:
            raise NotFound(
                'Post Does Not Exist'
            )
        data = Comments.query.filter_by(replyto=id).all()
        form = CommentForm()
        delform = DeleteForm()
        modifyform = CommentModifyForm()
        if form.validate_on_submit():
            comment = Comments(current_user.username, form.text.data, current_user.usertype, id)
            # print comment.text
            comment.add_comment()
            return redirect(url_for('forum_temp2', id=id))

        if modifyform.validate_on_submit():
            data = Comments.query.filter_by(id=modifyform.modifyid.data).first()
            data.modify_comment(modifyform.modifytext.data)
            return redirect(url_for('forum_temp2', id=id))

        if delform.id.data:
            deluser = Comments.query.filter_by(id=delform.id.data).first()
            deluser.delete_comment()
            replies = Comments.query.filter_by(replyto=delform.id.data).all()
            for reply in replies:
                reply.delete_comment()
            return redirect(url_for('forum_temp2', id=id))
        return render_template('forumtemp2.html', form=form, delform=delform, modform=modifyform, heading=heading, data=data,
                               loginform=loginform, user=current_user, postid=id)