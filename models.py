from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float
from datetime import datetime
from db_connection import db  # Utilisation de db.Model


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(Integer, primary_key=True)
    nom = db.Column(String(100), nullable=False)
    date = db.Column(String(10), nullable=False)
    horaire = db.Column(String(5), nullable=False)
    nombre_couverts = db.Column(Integer, nullable=False)
    code_reservation = db.Column(String(10), unique=True, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Reservation(id={self.id}, nom={self.nom}, date={self.date}, horaire={self.horaire}, couverts={self.nombre_couverts}, code={self.code_reservation})>"

class Commande(db.Model):
    __tablename__ = 'commandes'

    id = db.Column(Integer, primary_key=True)
    nom_client = db.Column(String(100), nullable=False)
    plats = db.Column(JSON, nullable=False)  # Liste des plats et quantités sous forme JSON
    heure_retrait = db.Column(String(5), nullable=False)  # Format HH:MM
    statut = db.Column(String(20), default="En attente")  # "En attente" ou "Prête"
    code_reservation = db.Column(String(10), ForeignKey('reservations.code_reservation'), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Commande(id={self.id}, nom={self.nom_client}, plats={self.plats}, heure={self.heure_retrait}, statut={self.statut}, code_reservation={self.code_reservation})>"

from db_connection import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # entrée, plat, dessert, boisson
    prix = db.Column(db.Float, nullable=False)
    quantite_disponible = db.Column(db.Integer, nullable=False)
    temps_preparation = db.Column(db.Integer, nullable=False)  # en minutes
