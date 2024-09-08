# Implementación del Microservicio de Gestión de Incidentes

from flask_sqlalchemy import SQLAlchemy
from app import db
import datetime


# ********* Paso 2: Definir el Modelo de la Base de Datos(SQLAlchemy) *********
db = SQLAlchemy()

class Incidente(db.Model):
    __tablename__ = 'incidentes'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    fecha_creacion = db.Column(
        db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
