# Creación del Microservicio de Autenticación y Autorización

from flask import Flask, request, jsonify
from app.models import db, Incidente
from functools import wraps
import jwt
import datetime


# ********* Paso 1: Implementar el endpoint de autenticación *********
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'

# Mock base de datos usuario
users = {
    "admin": "password123",
    "user": "password456"
}

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    username = auth.get('username')
    password = auth.get('password')

    # Validar credenciales de usuario
    if username in users and users[username] == password:
        token = jwt.encode({
            'username': username,
            'role': 'admin' if username == 'admin' else 'user',
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1) # Tiempo de expiración en UTC
        }, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401


# ********* Paso 3: Crear Endpoints de Incidentes *********
# Middleware de validación de tokens
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.role = data['role']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorator


@app.route('/incidentes', methods=['POST'])
@token_required
def crear_incidente():
    data = request.json
    nuevo_incidente = Incidente(
        descripcion=data['descripcion'], estado=data['estado'])
    db.session.add(nuevo_incidente)
    db.session.commit()
    return jsonify({'message': 'Incidente creado'}), 201


@app.route('/incidentes', methods=['GET'])
@token_required
def obtener_incidentes():
    incidentes = Incidente.query.all()
    output = [{'id': i.id, 'descripcion': i.descripcion,
               'estado': i.estado} for i in incidentes]
    return jsonify(output)


@app.route('/incidentes/<id>', methods=['DELETE'])
@token_required
def eliminar_incidente(id):
    if request.role != 'admin':
        return jsonify({'message': 'No tienes permisos'}), 403

    incidente = Incidente.query.get(id)
    if incidente:
        db.session.delete(incidente)
        db.session.commit()
        return jsonify({'message': 'Incidente eliminado'}), 200

    return jsonify({'message': 'Incidente no encontrado'}), 404
