from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE_URI = None
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

class Model(db.model):

    def __init__(self):
        pass

    def __repr__(self):
        pass