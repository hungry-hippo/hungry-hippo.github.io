# encoding=utf-8
import click

from expecto_judicio.application import create_app
from expecto_judicio.application import db, login_manager

app = create_app()

from expecto_judicio.models import User
from expecto_judicio.views import *

# No methods specified, so only available as GET
app.add_url_rule('/root', SamplePageRoot.endpoint, view_func=SamplePageRoot.as_view(SamplePageRoot.endpoint), methods=['GET','POST'])
app.add_url_rule('/login', SamplePageA.endpoint, view_func=SamplePageA.as_view(SamplePageA.endpoint), methods=['GET','POST'])
app.add_url_rule('/forum', SamplePageB.endpoint, view_func=SamplePageB.as_view(SamplePageB.endpoint), methods=['GET','POST'])
app.add_url_rule('/useraccess', SamplePageC.endpoint, view_func=SamplePageC.as_view(SamplePageC.endpoint), methods=['GET','POST'])
app.add_url_rule('/<name>', SamplePageD.endpoint, view_func=SamplePageD.as_view(SamplePageD.endpoint), methods=['GET','POST'])
app.add_url_rule('/legalpage', SamplePageE.endpoint, view_func=SamplePageE.as_view(SamplePageE.endpoint), methods=['GET','POST'])
app.add_url_rule('/logout', Logout.endpoint, view_func=Logout.as_view(Logout.endpoint), methods=['GET','POST'])

login_manager.login_view = 'sample_page_a'


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter(User.id == int(user_id)).first()
    except AttributeError:
        # User not found
        return None


@app.cli.command()
def create_db():
    import expecto_judicio.models  # import here because of circular imports

    click.echo('Creating all tables in database...')
    db.create_all()


@app.cli.command()
def drop_db():
    import expecto_judicio.models  # import here because of circular imports

    click.echo('Dropping all tables in database...')
    db.drop_all()


if __name__ == '__main__':
    # set debug to false when moving to production
    app.run(debug=True)
