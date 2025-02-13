from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db_connection import Base  # Assure-toi que Base est importé depuis db_connection

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    date = Column(String(100), nullable=False)  # Tu peux aussi utiliser Date si tu préfères stocker une vraie date
    horaire = Column(String(5), nullable=False)  # Horaire en format HH:MM
    nombre_couverts = Column(Integer, nullable=False)
    code_reservation = Column(String(10), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Reservation(id={self.id}, nom={self.nom}, date={self.date}, horaire={self.horaire}, couverts={self.nombre_couverts}, code={self.code_reservation})>"
