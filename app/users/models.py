from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db, BaseModelMixin

class Users(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

    order = db.relationship('Order', backref='Users', lazy=True)

    def __repr__(self):
        return f'<Users {self.username}>'
    
    def __str__(self):
        return f'<Users {self.username}'

    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email=email).first()