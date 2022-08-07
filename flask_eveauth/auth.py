from .models import Base
from .models import Permission
from .models import Role
from .models import User
from .utils import get_current_user
from .views import routes


class Auth:
    def __init__(self, app=None, db=None, autocommit=False):
        if app is not None:
            self.init_app(app, db, autocommit)

    def init_app(self, app, db=None, autocommit=False):
        app.extensions['eveauth'] = self
        register_blueprint(app)
        if db:
            init_tables(app, db, autocommit)
        register_template_context_processors(app)


def register_blueprint(app):
    app.register_blueprint(routes)


def init_tables(app, db, autocommit):
    if autocommit:
        with app.app_context():
            Base.metadata.create_all(db.engine)
    else:
        db.metadata._add_table('permission', None, Permission.__table__)
        db.metadata._add_table('role', None, Role.__table__)
        db.metadata._add_table('user', None, User.__table__)


def register_template_context_processors(app):
    @app.context_processor
    def inject_processors():
        return {
            'current_user': get_current_user()
        }
