import datetime
from application import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    abstract = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    creationDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)


