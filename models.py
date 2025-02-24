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

    # Relation avec Commande
    commandes = db.relationship('Commande', backref='reservation', lazy=True)

    def __repr__(self):
        return f"<Reservation(id={self.id}, nom={self.nom}, date={self.date}, horaire={self.horaire}, couverts={self.nombre_couverts}, code={self.code_reservation})>"

class Commande(db.Model):
    __tablename__ = 'commandes'

    id = db.Column(Integer, primary_key=True)
    nom_client = db.Column(String(100), nullable=False)
    plats = db.Column(JSON, nullable=False)  # Liste des plats et quantités sous forme JSON
    heure_retrait = db.Column(String(5), nullable=False)  # Format HH:MM
    statut = db.Column(String(20), default="En attente")  # "En attente" ou "Prête"
    total = db.Column(Float, nullable=False)  # Total de la commande
    code_reservation = db.Column(String(10), ForeignKey('reservations.code_reservation'), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Commande(id={self.id}, nom={self.nom_client}, plats={self.plats}, heure={self.heure_retrait}, statut={self.statut}, total={self.total}, code_reservation={self.code_reservation})>"

class CommandeItem(db.Model):
    __tablename__ = 'commande_items'

    id = db.Column(Integer, primary_key=True)
    commande_id = db.Column(Integer, ForeignKey('commandes.id'), nullable=False)
    plat_id = db.Column(Integer, ForeignKey('menus.id'), nullable=False)
    quantite = db.Column(Integer, nullable=False)
    prix_total = db.Column(Float, nullable=False)

    commande = db.relationship('Commande', back_populates="items")
    plat = db.relationship('Menu', backref='commande_items')

Commande.items = db.relationship('CommandeItem', back_populates='commande')

class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(Integer, primary_key=True)
    nom = db.Column(String(100), nullable=False)
    description = db.Column(String(255), nullable=False)
    type = db.Column(String(50), nullable=False)  # entrée, plat, dessert, boisson
    prix = db.Column(Float, nullable=False)
    quantite_disponible = db.Column(Integer, nullable=False)
    temps_preparation = db.Column(Integer, nullable=False)  # en minutes

    def __repr__(self):
        return f"<Menu(id={self.id}, nom={self.nom}, prix={self.prix}, quantite_disponible={self.quantite_disponible})>"
