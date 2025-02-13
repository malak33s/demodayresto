from flask import Flask, jsonify, request
from db_connection import db, engine
from models import Reservation
from flask_migrate import Migrate
import random  # Pour générer le code de réservation
from datetime import datetime, timedelta

# Créez l'application Flask
app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'  # Changez si nécessaire
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Pour éviter un avertissement

# Initialisation de SQLAlchemy
db.init_app(app)

# Initialisation de Flask-Migrate
migrate = Migrate(app, db)

# Créer les tables dans la base de données
with app.app_context():
    db.create_all()

# Nombre total de couverts disponibles
TOTAL_COUVERTS_DISPONIBLES = 50

# Définition des horaires par jour
HORAIRES_PAR_JOUR = {
    "lundi": [("12:00", "14:30"), ("19:00", "22:30")],
    "mardi": [("12:00", "14:30"), ("19:00", "22:30")],
    "mercredi": [("12:00", "14:30"), ("19:00", "22:30")],
    "jeudi": [("12:00", "14:30"), ("19:00", "22:30")],
    "vendredi": [("12:00", "14:30"), ("19:00", "22:30")],
    "samedi": [("12:00", "15:00"), ("19:00", "23:00")],
    "dimanche": []  # Fermé
}

@app.route('/horaires-disponibles', methods=['GET'])
def horaires_disponibles():
    date = request.args.get('date')
    if not date:
        return jsonify({"message": "La date est requise"}), 400

    jour_semaine = datetime.strptime(date, "%Y-%m-%d").strftime("%A").lower()
    if jour_semaine not in HORAIRES_PAR_JOUR or not HORAIRES_PAR_JOUR[jour_semaine]:
        return jsonify({"message": "Le restaurant est fermé ce jour-là"}), 400

    horaires_possibles = []
    for debut, fin in HORAIRES_PAR_JOUR[jour_semaine]:
        heure_actuelle = datetime.strptime(debut, "%H:%M")
        heure_fin = datetime.strptime(fin, "%H:%M")
        while heure_actuelle < heure_fin:
            horaire_str = heure_actuelle.strftime("%H:%M")
            couverts_reserves = sum(res.nombre_couverts for res in db.session.query(Reservation).filter_by(date=date, horaire=horaire_str))
            places_restantes = TOTAL_COUVERTS_DISPONIBLES - couverts_reserves
            if places_restantes > 0:
                horaires_possibles.append({"horaire": horaire_str, "places_restantes": places_restantes})
            heure_actuelle += timedelta(minutes=30)

    return jsonify(horaires_possibles)

@app.route('/reservations', methods=['POST'])
def reserver_table():
    """Créer une nouvelle réservation en vérifiant la disponibilité et l'horaire."""
    data = request.get_json()

    nom = data.get('nom')
    date = data.get('date')
    horaire = data.get('horaire')
    nombre_couverts = data.get('nombre_couverts')

    if not nom or not date or not horaire or not nombre_couverts:
        return jsonify({"message": "Tous les champs sont requis (nom, date, horaire, nombre_couverts)"}), 400

    jour_semaine = datetime.strptime(date, "%Y-%m-%d").strftime("%A").lower()
    if jour_semaine not in HORAIRES_PAR_JOUR or not any(debut <= horaire <= fin for debut, fin in HORAIRES_PAR_JOUR[jour_semaine]):
        return jsonify({"message": "Horaire non disponible"}), 400

    # Vérifier le nombre de couverts déjà réservés à cette date et cet horaire
    couverts_reserves = db.session.query(Reservation).filter_by(date=date, horaire=horaire).all()
    total_reserves = sum(res.nombre_couverts for res in couverts_reserves)

    if total_reserves + nombre_couverts > TOTAL_COUVERTS_DISPONIBLES:
        return jsonify({"message": "Nombre de couverts insuffisant pour cette date et cet horaire"}), 400

    # Générer un code de réservation unique
    nouveau_code = str(random.randint(1000, 9999))

    # Créer la réservation
    nouvelle_reservation = Reservation(
        nom=nom,
        date=date,
        horaire=horaire,
        nombre_couverts=nombre_couverts,
        code_reservation=nouveau_code
    )

    db.session.add(nouvelle_reservation)
    db.session.commit()

    return jsonify({"message": "Réservation effectuée", "code_reservation": nouveau_code}), 201

@app.route('/reservations', methods=['GET'])
def get_reservations():
    """Obtenir toutes les réservations"""
    reservations = db.session.query(Reservation).all()
    result = [{"nom": res.nom, "date": res.date, "horaire": res.horaire, "nombre_couverts": res.nombre_couverts, "code": res.code_reservation} for res in reservations]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
