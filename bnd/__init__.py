from flask import Flask
from flask.ext.login import LoginManager
from logbook import Logger
import os


log = Logger()
login_manager = LoginManager()


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

    from bnd.curriculum import curriculum_module
    from bnd.checkpoint import checkpoint_module
    from bnd.team import team_module
    from bnd.goal import goal_module
    from bnd.user import user_module

    # Blueprint modules
    app.register_blueprint(curriculum_module, url_prefix='/curriculum')
    app.register_blueprint(team_module, url_prefix='/team')
    app.register_blueprint(checkpoint_module, url_prefix='/checkpoint')
    app.register_blueprint(goal_module, url_prefix='/goal')
    app.register_blueprint(user_module, url_prefix='/user')

    return app
