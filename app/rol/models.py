from app.db import db, BaseModelMixin

class Rol(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    user = db.relationship('Users', backref='Rol', lazy=True)