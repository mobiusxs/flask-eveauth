from .models import Base
from .models import Role
from .models import Session
from .models import Token
from .models import User
from .views import routes


class Auth:
    def __init__(self, app=None, db=None, autocommit=False):
        if app is not None:
            self.init_app(app, db, autocommit)

    def init_app(self, app, db=None, autocommit=False):
        app.extensions['eveauth'] = self
        register_blueprint(app)
        if db:
            init_tables(db, autocommit)

        @app.before_request()
        def before_func():
            pass

        @app.teardown_request()
        def teardown_func():
            pass


def register_blueprint(app):
    app.register_blueprint(routes)


def init_tables(db, autocommit):
    if autocommit:
        Base.metadata.create_all(db.engine)
    else:
        db.metadata._add_table('role', None, Role.__table__)
        db.metadata._add_table('session', None, Session.__table__)
        db.metadata._add_table('token', None, Token.__table__)
        db.metadata._add_table('user', None, User.__table__)
