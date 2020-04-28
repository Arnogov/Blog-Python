from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import redirect, url_for
import os

app = Flask(__name__)
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
