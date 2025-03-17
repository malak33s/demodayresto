from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from db_connection import db  # Connexion à la base via Flask SQLAlchemy

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(Integer, primary_key=True)
    nom = db.Column(String(100), nullable=False)
    date = db.Column(String(10), nullable=False)
    horaire = db.Column(Time, nullable=False)
    nombre_couverts = db.Column(Integer, nullable=False)
    code_reservation = db.Column(String(10), unique=True, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

    # Relation avec Commande
    commandes = db.relationship('Commande', back_populates='reservation')

    def __repr__(self):
        return f"<Reservation(id={self.id}, nom={self.nom}, date={self.date}, horaire={self.horaire}, couverts={self.nombre_couverts}, code={self.code_reservation})>"

class Commande(db.Model):
    __tablename__ = 'commandes'

    id = db.Column(Integer, primary_key=True)
    nom_client = db.Column(String(100), nullable=False)
    heure_retrait = db.Column(Time, nullable=False)  # Format HH:MM
    statut = db.Column(String(20), default="En attente")  # "En attente" ou "Prête"
    total = db.Column(Float, nullable=False)  # Total de la commande
    created_at = db.Column(DateTime, default=datetime.utcnow)

    # Relation optionnelle avec Reservation
    code_reservation = db.Column(String(10), ForeignKey('reservations.code_reservation'), nullable=True)
    reservation = db.relationship('Reservation', back_populates='commandes')

    # Relation avec les plats
    items = db.relationship('CommandeItem', back_populates='commande', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Commande(id={self.id}, nom={self.nom_client}, heure={self.heure_retrait}, statut={self.statut}, total={self.total})>"

class CommandeItem(db.Model):
    __tablename__ = 'commande_items'

    id = db.Column(Integer, primary_key=True)
    commande_id = db.Column(Integer, ForeignKey('commandes.id'), nullable=False)
    plat_id = db.Column(Integer, ForeignKey('menus.id'), nullable=False)
    quantite = db.Column(Integer, nullable=False)
    prix_total = db.Column(Float, nullable=False)

    # Relations
    commande = db.relationship('Commande', back_populates='items')
    plat = db.relationship('Menu')

    def __repr__(self):
        return f"<CommandeItem(id={self.id}, commande={self.commande_id}, plat={self.plat_id}, quantite={self.quantite}, prix_total={self.prix_total})>"

class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(Integer, primary_key=True)
    nom = db.Column(String(100), nullable=False)
    description = db.Column(String(255), nullable=False)
    type = db.Column(String(50), nullable=False)
    prix = db.Column(Float, nullable=False)
    quantite_disponible = db.Column(Integer, nullable=False)
    temps_preparation = db.Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Menu(id={self.id}, nom={self.nom}, type={self.type}, prix={self.prix})>"
