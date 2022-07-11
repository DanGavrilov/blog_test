from datetime import datetime
from flask_login import UserMixin

from sweater import db


class User(db.Model, UserMixin):
    tablename = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    articles = db.relationship("Article", lazy='dynamic', primaryjoin='foreign(Article.author_id) == User.id')

    def repr(self):
        return '<User %r>' % self.id


class Article(db.Model):
    tablename = 'Articles'
    id = db.Column(db.Integer, primary_key=True)
    posts = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer)
    author = db.relationship('User', primaryjoin='foreign(Article.author_id) == User.id')

    def repr(self):
        return '<Article %r>' % self.id