from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, UserMixin, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///like_twitter_but_not_twitter.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manage = LoginManager(app)
app.secret_key = 'LHIOhbjdkjbhskjfi118278bksdjdbhfh'


class User(db.Model, UserMixin):
    __tablename__='Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Article(db.Model):
    __tablename__='Articles'
    author_id = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    posts = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def registration_is_success(login, audit_password):
    registration = True
    filter = User.query.filter_by(login=login).first()
    if filter != None or audit_password != True:
        registration = False
    return registration


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        login = request.form['login']
        password = generate_password_hash(request.form['password'])
        audit_password = check_password_hash(password, request.form['audit'])
        audit = registration_is_success(login, audit_password)
        if audit == True:
            user = User(name=name, login=login, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        else:
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/my')
@login_required
def user_page():
    articles = Article.query.order_by(Article.date.desc()).filter_by(author_id=current_user.id)
    return render_template('user_page.html', articles=articles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/my')
        else:
            flash('Неправильний логін або пароль')

    else:
        return render_template('login_user.html')
    return render_template('login_user.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/',  methods=['GET', 'POST'])
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('index.html', articles=articles)


@app.route('/main',  methods=['GET', 'POST'])
def main_page():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('main_page.html', articles=articles)


@app.route('/<int:id>/delete')
def delete(id):
    articles = Article.query.get_or_404(id)
    db.session.delete(articles)
    db.session.commit()
    return redirect('/my')


@app.route('/<int:id>/del')
@login_required
def del_user(id):
    users = User.query.get_or_404(id)
    db.session.delete(users)
    db.session.commit()
    return redirect('/my')


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
       author_id = current_user.id
       name = current_user.name
       posts = request.form['posts']
       new_post = Article( posts=posts, author_id=author_id, author_name=name)
       db.session.add(new_post)
       db.session.commit()
       return redirect('/my')
    else:
        return render_template('create_post.html')


if __name__ == '__main__':

    app.run(debug=True)

