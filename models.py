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

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(Integer, primary_key=True)
    nom = db.Column(String(100), unique=True, nullable=False)
    description = db.Column(String(255), nullable=True)
    type = db.Column(String(50), nullable=False)  # "entrée", "plat", "dessert", "boisson", etc.
    prix = db.Column(Float, nullable=False)

    def __repr__(self):
        return f"<Menu(id={self.id}, nom={self.nom}, type={self.type}, prix={self.prix})>"
