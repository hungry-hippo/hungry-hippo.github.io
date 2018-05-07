from expecto_judicio.application import db, create_app
app = create_app()
app.app_context().push()  # normally, you wrap this in a with ...: call, this is what it does internally, it's already present when you are in a view method, so you don't worry about it normally
from expecto_judicio.models import *
db.create_all()

#admin = User('admin', 'admin', 3)
#guest = User('Baisakhi', '123456', 1)
#guest2 = User('Avimita', '123456', 2)
#db.session.add(admin)
#db.session.add(guest)
#db.session.add(guest2)
#db.session.commit()