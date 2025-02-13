from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Utiliser un contexte d'application pour créer l'engine
with app.app_context():
    engine = db.engine

Base = db.Model
