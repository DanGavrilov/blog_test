from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///like_twitter_but_not_twitter.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manage = LoginManager(app)
app.secret_key = 'LHIOhbjdkjbhskjfi118278bksdjdbhfh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

