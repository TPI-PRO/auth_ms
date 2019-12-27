from app import db,login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#True is admin
#Public-id for security
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    nombres = db.Column(db.String(100),index=True,nullable=False)
    apellidos = db.Column(db.String(100),index=True,nullable=True)
    username = db.Column(db.String(64), index=True, unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(120), index=True, unique=True,nullable=False)
    rol = db.Column(db.Boolean,default=True,nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    fecha = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)