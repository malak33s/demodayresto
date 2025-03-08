from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text  # Ajoute cette ligne

app = Flask(__name__)
cors = CORS(app)

# Connexion à MySQL
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_NAME = "demoday_db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Fonction pour insérer les données par défaut dans la base
def insert_default_data():
    with app.app_context():  # Création d'un contexte d'application
        existing_menus = db.session.execute(text("SELECT COUNT(*) FROM menus")).scalar()  # La fonction 'text' est maintenant importée
        if existing_menus == 0:
            # Insertion des données par défaut pour les menus
            menu_items = [
                {"nom": "Brick", "description": "Brick", "type": "Entrée", "prix": 2.90, "quantite_disponible": 30, "temps_preparation": 20},
                {"nom": "Slata Méchouia", "description": "Slata Méchouia", "type": "Entrée", "prix": 3.50, "quantite_disponible": 30, "temps_preparation": 15},
                {"nom": "Fricassée", "description": "Fricassée", "type": "Plat", "prix": 1.90, "quantite_disponible": 30, "temps_preparation": 10},
                {"nom": "Riz Djerbien", "description": "Riz Djerbien", "type": "Plat", "prix": 13.90, "quantite_disponible": 30, "temps_preparation": 30},
                {"nom": "Nwasser", "description": "Nwasser", "type": "Plat", "prix": 12.90, "quantite_disponible": 30, "temps_preparation": 25},
                {"nom": "Couscous Tunisien", "description": "Couscous Tunisien", "type": "Plat", "prix": 16.50, "quantite_disponible": 30, "temps_preparation": 40},
                {"nom": "Chakchouka", "description": "Chakchouka", "type": "Plat", "prix": 10.90, "quantite_disponible": 30, "temps_preparation": 20},
                {"nom": "Baklawa", "description": "Baklawa", "type": "Dessert", "prix": 3.90, "quantite_disponible": 30, "temps_preparation": 10},
                {"nom": "Makrout", "description": "Makrout", "type": "Dessert", "prix": 2.90, "quantite_disponible": 30, "temps_preparation": 15},
                {"nom": "Zrir", "description": "Zrir", "type": "Dessert", "prix": 2.90, "quantite_disponible": 30, "temps_preparation": 10},
                {"nom": "Ice tea pêche", "description": "Ice tea pêche", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Ice tea framboise", "description": "Ice tea framboise", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Coca Cola Zero", "description": "Coca Cola Zero", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Coca Cola Original", "description": "Coca Cola Original", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Coca Cola Cherry", "description": "Coca Cola Cherry", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Oasis Tropical", "description": "Oasis Tropical", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Oasis Pomme, cassis, framboise", "description": "Oasis Pomme, cassis, framboise", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Perrier", "description": "Perrier", "type": "Boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2},
                {"nom": "Eau Abatilles", "description": "Eau Abatilles", "type": "Boisson", "prix": 1.50, "quantite_disponible": 50, "temps_preparation": 1.5},
                {"nom": "Café arabe", "description": "Café arabe", "type": "Boisson", "prix": 2.50, "quantite_disponible": 50, "temps_preparation": 5},
                {"nom": "Thé rouge tunisien", "description": "Thé rouge tunisien", "type": "Boisson", "prix": 2.50, "quantite_disponible": 50, "temps_preparation": 5},
                {"nom": "Espresso", "description": "Espresso", "type": "Boisson", "prix": 2.50, "quantite_disponible": 50, "temps_preparation": 5},
            ]
            
            # Ajout des éléments au menu
            for item in menu_items:
                menu = Menu(**item)  # Utilisation de la classe Menu (définie ailleurs)
                db.session.add(menu)
            db.session.commit()

# Lancer la fonction d'insertion de données par défaut
insert_default_data()

if __name__ == "__main__":
    app.run(debug=True)
