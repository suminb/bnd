from flask import Flask
import os


app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['DEBUG'] = True
