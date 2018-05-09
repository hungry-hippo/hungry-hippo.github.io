# encoding=utf-8
import click

from expecto_judicio.application import create_app
from expecto_judicio.application import db, login_manager

app = create_app()

from expecto_judicio.config import SQLALCHEMY_TRACK_MODIFICATIONS
from expecto_judicio.models import User
from expecto_judicio.views import *

# No methods specified, so only available as GET
#app.add_url_rule('/scc', TrackCases.endpoint, view_func=TrackCases.as_view(TrackCases.endpoint), methods=['GET','POST'])
app.add_url_rule('/scc/<id>', TrackCaseResult.endpoint, view_func=TrackCaseResult.as_view(TrackCaseResult.endpoint), methods=['GET','POST'])
app.add_url_rule('/home', HomePage.endpoint, view_func=HomePage.as_view(HomePage.endpoint), methods=['GET','POST'])
app.add_url_rule('/useraccess', ManageUsers.endpoint, view_func=ManageUsers.as_view(ManageUsers.endpoint), methods=['GET','POST'])
app.add_url_rule('/searchresults/<name>', SearchResults.endpoint, view_func=SearchResults.as_view(SearchResults.endpoint), methods=['GET','POST'])
app.add_url_rule('/legalpage', LegalDatabaseAccess.endpoint, view_func=LegalDatabaseAccess.as_view(LegalDatabaseAccess.endpoint), methods=['GET','POST'])
app.add_url_rule('/logout', Logout.endpoint, view_func=Logout.as_view(Logout.endpoint), methods=['GET','POST'])
app.add_url_rule('/forum', Forum1.endpoint, view_func=Forum1.as_view(Forum1.endpoint), methods=['GET','POST'])
app.add_url_rule('/forum/<id>', Forum2.endpoint, view_func=Forum2.as_view(Forum2.endpoint), methods=['GET','POST'])
app.add_url_rule('/', RootPage.endpoint, view_func=RootPage.as_view(RootPage.endpoint), methods=['GET','POST'])
app.add_url_rule('/<var>', WrongUrl.endpoint, view_func=WrongUrl.as_view(WrongUrl.endpoint), methods=['GET','POST'])

#login_manager.login_view =  HomePage.endpoint


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter(User.id == int(user_id)).first()
    except AttributeError:
        # User not found
        return None


@app.cli.command()
def create_db():
    import models  # import here because of circular imports

    click.echo('Creating all tables in database...')
    db.create_all()


@app.cli.command()
def drop_db():
    import models  # import here because of circular imports

    click.echo('Dropping all tables in database...')
    db.drop_all()


if __name__ == '__main__':
    # set debug to false when moving to production
    app.run()
