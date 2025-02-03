from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Resto(Base):
    __tablename__ = 'restos'  # Nom de la table dans la base de données
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    address = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)  # Valeur par défaut pour l'heure de création

# Si tu veux créer des tables dans ta base de données, voici comment procéder :
from sqlalchemy import create_engine

# Remplace par les mêmes infos de connexion que dans db_connection.py
engine = create_engine(f'mysql+mysqlclient://root:ton_mot_de_passe@localhost/nom_de_ta_base_de_donnees')

# Créer toutes les tables définies dans les modèles
Base.metadata.create_all(engine)
