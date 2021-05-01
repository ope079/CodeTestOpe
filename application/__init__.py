from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)


app.config['SECRET_KEY'] = "SECRET_KEY"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:/sqlite/test.db"

db = SQLAlchemy(app)



from application import routes