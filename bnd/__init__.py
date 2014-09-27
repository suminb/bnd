from flask import Flask
from bnd.curriculum import curriculum_module
import os


app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['DEBUG'] = True

app.register_blueprint(curriculum_module, url_prefix='/curriculum')
