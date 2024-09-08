import os

# Configurar la Aplicación Flask para usar PostgreSQL localmente
class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/incidentes_db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/incidentes_db'
    SECRET_KEY = 'clave_secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
