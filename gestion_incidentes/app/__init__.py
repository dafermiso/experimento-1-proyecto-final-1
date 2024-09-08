# Inicializar la Base de Datos desde Flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context(): #asegura que las tablas se creen dentro del contexto de la aplicación Flask.
        db.create_all()

    return app
