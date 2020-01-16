from app import db,app
from flask import request, jsonify
from app.models import User
import uuid
from flask_login import current_user,logout_user,login_user
import jwt 
import datetime
import json



@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users',methods=['GET','DELETE','POST','PUT'])
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
                        user_data['email']=user.email
                        user_data['rol']=user.rol
                        user_data['descripcion']=user.descripcion
                        user_data['fecha']=user.fecha
                        output.append(user_data)
                return jsonify(output)
        if request.method == 'DELETE':
                db.session.query(User).delete()
                db.session.commit()
                if len(User.query.all()) == 0:
                        return jsonify({'mensaje': 'Eliminacion de usuarios satisfactoria!'})
                return jsonify({'mensaje':'No se pudo eliminar a los usuarios'})
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

        if request.method == 'PUT':
                public_id = request.json['public_id']
                user = User.query.filter_by(public_id=public_id).first()
                if user == None:
                        return jsonify({'mensaje':'No existe el usuario'})
                user.nombres=request.json['nombres']
                user.apellidos=request.json['apellidos']
                varuser = request.json['username']
                if User.query.filter_by(username=varuser).first() is not None:
                        return jsonify({'mensaje':'Ese usuario ya existe por favor seleccione otro'})
                user.username=varuser
                user.rol=request.json['rol']
                user.descripcion=request.json['descripcion']
                db.session.commit()
                return jsonify({'mensaje':'Actualizacion exitosa'})

#Some basic search by username or email
@app.route('/users/username/<username>',methods=['GET','DELETE'])
def searchbyUsername(username):
        if request.method == 'GET':
                user = User.query.filter((User.username==username) | (User.email==username) ).first()
                if user == None:
                        return jsonify({'mensaje':'Ese usuario no existe'})
                conv = {}
                conv['public_id'] = user.public_id
                conv['nombres'] = user.nombres
                conv['apellidos'] = user.apellidos
                conv['username']=user.username
                conv['email']=user.email
                conv['rol']=user.rol
                conv['descripcion']=user.descripcion
                conv['fecha']=user.fecha
                return jsonify(conv)
        if request.method == 'DELETE':
                User.query.filter((User.username==username)|(User.email==username)).delete()
                db.session.commit()
                return jsonify({'mensaje':'Usuario eliminado correctamente'})
       
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
                return jsonify(token.decode('UTF-8'))

#Default method get
@app.route('/users/logout')
def logout():
        logout_user()
        return "Log out exitoso"
