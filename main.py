from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///like_twitter_but_not_twitter.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('index.html', articles=articles)


@app.route('/<int:id>/delete')
def delete(id):
    articles = Article.query.get_or_404(id)
    db.session.delete(articles)
    db.session.commit()
    return redirect('/')


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
       name = request.form['name']
       posts = request.form['posts']
       new_post = Article(name=name, posts=posts)
       db.session.add(new_post)
       db.session.commit()
       return redirect('/')
    else:
        return render_template('create_post.html')


if __name__ == '__main__':
    app.run(debug=True)


