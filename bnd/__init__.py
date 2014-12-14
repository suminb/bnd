from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from logbook import Logger
from bnd.models import db, User, Team, Checkpoint, Goal, Evaluation, Application
import os


log = Logger()
login_manager = LoginManager()
admin = Admin()


class AdminIndexView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


#admin.index_view = AdminIndexView


def create_app(config_filename):
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    app.secret_key = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    app.config['DEBUG'] = True

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

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


    admin.init_app(app)
    classes = [User, Team, Checkpoint, Goal, Evaluation]
    for cls in classes:
        admin.add_view(ModelView(cls, db.session, endpoint='admin_'+cls.__name__))

    return app
