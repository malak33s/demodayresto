from db_connection import db
from models import Reservation

# Vérifier la connexion
try:
    with db.engine.connect() as connection:
        print(" Connexion à la base de données réussie !")
except Exception as e:
    print(f" Erreur de connexion : {e}")
