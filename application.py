from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import redirect, url_for
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
# Récupération du chemin du fichier de la base de données
dbPath = os.path.join(app.root_path, 'blog.db')
if not os.path.exists(dbPath):
    db.create_all()
    print("Base de données créée")
# Tableau pour stocker nos tweets
posts = []

@app.route('/')
def hello_world():
    return 'Hello World!'
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/users/create', methods=['POST', 'GET'])
def create_user():
    # Si la méthode est de type "GET"
    if request.method == 'GET':
        # On affiche notre formulaire de création
        return render_template('create_user.html')
    else:
        # Sinon, notre méthode HTTP est POST
        # on va donc créer un nouvel utilisateur
        # récupération du nom de l'utilisateur depuis le corps de la requête
        name = request.form['name']
        # récupération de l'email depuis le corps de la requête
        email = request.form['email']
        # récupération du mot de passe depuis le corps de la requête
        password = request.form['password']
        # Création d'un utilisateur à l'aide du constructeur généré par SQLAlchemy
        user = User(name=name, email=email, password=password)
        # Insertion de notre utilisateur dans session de base de données
        # Attention, celui-ci n'est pas encore présent dans la base de données
        db.session.add(user)
        # Sauvegarde de notre session dans la base de données
        db.session.commit()
        # Redirection vers la liste de nos tweets
        return redirect(url_for('display_users'))

    # Association de la route "/login" à notre fonction login()
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Si on est dans une requête GET
        if request.method == 'GET':
            # On affiche simplement le formulaire de Login
            return render_template('login.html')
        else:
            # Sinon cela veut dire qu'on est dans une méthode POST
            # On récupère l'utilisateur avec son email
            user = User.query.filter_by(email=request.form['email']).first()
            # Si notre utilisteur existe et
            # Si le mot de passe présent dans le formulaire est le même que celui de la base de données
            if user != None and user.password == request.form['password']:
                # On a réussi notre login, on inscrit donc le l'identifiant de l'utilisateur dans la variable de session
                session['user_id'] = user.id
                # on redirige l'utilisateur vers la liste des tweets
                return redirect(url_for('display_posts'))
            else:
                # Si l'utilisateur n'existe pas ou que les mots de passes ne correspondent pas
                # on renvoie l'utilisateur vers le formulaire de login.
                return render_template('login.html', error="Email et/ou mot de passe incorrect")

    # Association de la route "/logout" à notre fonction logout()
    @app.route('/logout')
    def logout():
        # Pour déconnecter l'utilisateur on enlève user_id de la variable session
        session.pop('user_id', None)
        return redirect(url_for('display_posts'))



