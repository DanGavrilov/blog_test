from sweater import login_manage, app, db
from sweater.models import User, Article
from flask import render_template, redirect, request, flash
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def registration_is_success(login, audit_password, name):
    registration = True
    filter = User.query.filter_by(login=login).first()
    if filter != None or audit_password != True or name == "" or login == "":
        registration = False
    return registration


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        login = request.form['login']
        password = generate_password_hash(request.form['password'])
        audit_password = check_password_hash(password, request.form['audit'])
        audit = registration_is_success(login, audit_password, name)
        if audit:
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
    user = current_user
    name = user.name
    articles = user.articles
    users = User.query.all()
    return render_template('user_page.html', articles=articles, name=name, users=users)


@app.route('/login', methods=['GET', 'POST'])
def log_in():
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


@app.route('/<int:id>/delete', methods=['DELETE', 'GET'])
@login_required
def del_it(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/my')


@app.route('/<int:id>/del', methods=['DELETE', 'GET'])
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
       posts = request.form['posts']
       new_post = Article(posts=posts, author_id=author_id)
       db.session.add(new_post)
       db.session.commit()
       return redirect('/my')
    else:
        return render_template('create_post.html')