# encoding=utf-8
from functools import wraps

from flask import render_template
from flask_login import current_user, login_required

from werkzeug.exceptions import Forbidden

#function called for system-admin access
def system_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            # TODO: change this to whatever your implementation becomes
            if current_user.usertype != 3:
                render_template('forbidden.html',
                                      msg='You do not have the rights to visit this page. Only available to system admins.')
            return func(*args, **kwargs)
        except AttributeError:
            # current_user is None => user not logged in
            return login_required(func)(*args, **kwargs)
    return decorated_view

#function called for legal-expert access
def legal_expert_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            # TODO: change this to whatever your implementation becomes
            if current_user.usertype != 2:
                render_template('forbidden.html', msg='You do not have the rights to visit this page. '
                                                      'Only available to legal experts.')
            return func(*args, **kwargs)
        except AttributeError:
            # current_user is None => user not logged in
            return login_required(func)(*args, **kwargs)

    return decorated_view


def system_admin_or_legal_expert_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            # TODO: change this to whatever your implementation becomes
            if current_user.usertype not in [3, 2]:
                render_template('forbidden.html', msg='You do not have the rights to visit this page. '
                                                      'Only available to system admins or legal experts.'
                )
            return func(*args, **kwargs)
        except AttributeError:
            # current_user is None => user not logged in
            return login_required(func)(*args, **kwargs)

    return decorated_view
