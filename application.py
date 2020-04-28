# Import de fonctions depuis le Framework Flask
from flask import Flask
# Import d'une fonction pour convertir un template HTML en y injectant des variables python
from flask import render_template
from flask import request
from flask import redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from variables import session_secret
from flask import session


from datetime import datetime

app = Flask(__name__)
app.secret_key = session_secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

from post import Post
from user import User

dbPath = os.path.join(app.root_path, 'blog.db')
if not os.path.exists(dbPath):
    db.create_all()
    print("Base de données créée")

posts = []


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/users/create', methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('display_users'))


@app.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        abort(404)
    if request.method == 'GET':
        return render_template('edit_user.html', user=user)
    else:
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('display_users'))

@app.route('/users')
def display_users():
    allUsers = User.query.all()
    return render_template('users.html', users=allUsers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = User.query.filter_by(email=request.form['email']).first()
        if user != None and user.password == request.form['password'] :
            session['user_id'] = user.id
            return redirect(url_for('display_posts'))
        else:
            return render_template('login.html', error="Email et/ou mot de passe incorrect")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('display_posts'))


@app.route('/posts')
def display_posts():
    allPosts = Post.query.all()
    user = None
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
    return render_template('posts.html', posts=allPosts, user=user)

@app.route('/posts/<int:user_id>')
def display_author_posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        abort(404)
    authorPosts = user.posts
    return render_template('posts.html', posts=authorPosts)


@app.route('/posts/create', methods=['POST', 'GET'])
def display_create_post():
    if not 'user_id' in session :
        return redirect(url_for('login'))
    if request.method == 'GET':
        users = User.query.all()
        return render_template('create_post.html', users=users)
    else:
        user_id = session['user_id']
        content = request.form['content']
        image = None
        f = request.files['image']
        if f.filename != '' :
            filepath = os.path.join(app.root_path, 'static', 'uploads', f.filename)
            f.save(filepath)
            image = url_for('static', filename='uploads/'+f.filename)
        post = Post(user_id=user_id, content=content, image=image)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('display_posts'))


@app.route('/posts/<int:post_id>/edit', methods=['POST', 'GET'])
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post == None:
        abort(404)
    if request.method == 'GET':
        users = User.query.all()
        return render_template('edit_post.html', post=post, users=users)
    else:
        post.user_id = request.form['user_id']
        post.content = request.form['content']
        f = request.files['image']
        if f.filename != '' :
            filepath = os.path.join(app.root_path, 'static', 'uploads', f.filename)
            f.save(filepath)
            post.image = url_for('static', filename='uploads/'+f.filename)
        db.session.commit()
        return redirect(url_for('display_posts'))
