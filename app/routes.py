from app import db,app
from flask import request, jsonify
from app.models import User
import uuid
from flask_login import current_user,logout_user,login_user
import jwt 
import datetime



@app.route('/')
def index():
    return "Hello, World! Andres"

@app.route('/users',methods=['GET'])
def users():
        if request.method=='GET':
                people=User.query.all()
                output = []
                for user in people:
                        user_data = {}
                        user_data['public_id'] = user.public_id
                        user_data['nombres'] = user.nombres
                        user_data['apellidos'] = user.apellidos
                        user_data['username']=user.username
                        output.append(user_data)
                return jsonify({'users' : output})

@app.route('/users/sign',methods=['POST'])
def signup():
        if request.method == 'POST':
                nombres=request.json['nombres']
                apellidos=request.json['apellidos']
                username=request.json['username']
                email=request.json['email']
                rol=request.json['rol']
                descripcion=request.json['descripcion']
                fecha=request.json['fecha']

                user = User.query.filter_by(username=username).first()
                if user is not None:
                        return "Usuario repetido"
                mail = User.query.filter_by(email=email).first()
                if mail is not None:
                        return "Correo no valido"

                person=User(public_id=str(uuid.uuid4()),nombres=nombres,apellidos=apellidos,username=username,email=email,rol=rol,descripcion=descripcion)
                person.set_password(request.json['password'])
                db.session.add(person)
                db.session.commit()
                return jsonify({'mensaje' : 'Nuevo usuario creado!'})

@app.route('/users/login',methods=['POST'])
def login():
        if request.method == 'POST':
                username=request.json['username']
                password=request.json['password']

                usuario=User.query.filter_by(username=username).first()
                if usuario is None or not usuario.check_password(password):
                        return "No logueado"
                token = jwt.encode({'public_id':usuario.public_id,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
                login_user(usuario)
                return jsonify({'token':token.decode('UTF-8')})

#Default method get
@app.route('/users/logout')
def logout():
        logout_user()
        return "Log out exitoso"
