"# Blog-Python" 
Activer l'environnement virtuel
. venv\Scripts\activate

installer Flask dans l'environnement virtuel
pip3 install flask

lancer l'application
set FLASK_APP=application.py

Automatisation mise à jour
set FLASK_ENV=development

lancer le run
python -m flask run
ou 
flask run

base de données
from application import db 
db.create_all()

