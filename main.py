from models import Resto
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db_connection import engine  # Importer l'engine de la connexion à la base de données

# Créer une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()

# Ajouter un nouveau restaurant
new_resto = Resto(
    name="Restaurant Exemple",
    address="123 Rue Exemple, Paris"
)

# Ajouter et valider les modifications dans la base de données
session.add(new_resto)
session.commit()

print("Restaurant ajouté avec succès !")
