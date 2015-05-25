from flask import Flask
from flask.ext.login import LoginManager, current_user
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.redis import FlaskRedis
from logbook import Logger
import os


__version__ = '0.9.4'


log = Logger()
login_manager = LoginManager()
redis_store = FlaskRedis()


ADMINS = [
    'suminb@gmail.com',
    'seth.ahn@gmail.com',
    'beingndoing.chair@gmail.com',
]


class AdminModelView(ModelView):
    #@expose('/')
    #def index(self):
    #    return self.render('index.html')

    def is_accessible(self):
        return not current_user.is_anonymous() and \
            current_user.email in ADMINS


# FIXME: Refacfor the following section
def checkpoint_status_class(status):
    if status == 'Completed':
        return 'label-success'
    elif status == 'Past-due':
        return 'label-danger'
    else:
        return 'label-default'


def create_app(name=__name__, config={},
               static_folder='static', template_folder='templates'):
    """NOTE: `db_uri` is only a temporary solution. It shall be replaced by
    something more robust."""
    app = Flask(name, static_folder=static_folder, template_folder=template_folder)
    app.secret_key = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    app.config['DEBUG'] = True
    app.config['REDIS_URL'] = os.environ.get(
        'REDIS_URL', 'redis://:password@localhost:6379/0')

    app.config.update(config)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    redis_store.init_app(app)

    from bnd.models import db
    db.init_app(app)

    from bnd.main import main_module
    from bnd.curriculum import curriculum_module
    from bnd.checkpoint import checkpoint_module
    from bnd.team import team_module
    from bnd.goal import goal_module
    from bnd.user import user_module

    # Blueprint modules
    app.register_blueprint(main_module, url_prefix='/')
    app.register_blueprint(curriculum_module, url_prefix='/curriculum')
    app.register_blueprint(team_module, url_prefix='/team')
    app.register_blueprint(checkpoint_module, url_prefix='/checkpoint')
    app.register_blueprint(goal_module, url_prefix='/goal')
    app.register_blueprint(user_module, url_prefix='/user')

    from bnd.models import User, Team, Checkpoint, Goal, Evaluation

    admin = Admin()
    admin.init_app(app)
    classes = [User, Team, Checkpoint, Goal, Evaluation]
    for cls in classes:
        admin.add_view(AdminModelView(cls, db.session, endpoint='admin_' + cls.__name__))

    app.jinja_env.globals.update(checkpoint_status_class=checkpoint_status_class)

    return app
