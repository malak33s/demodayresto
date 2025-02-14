from flask import Flask, jsonify, request
from db_connection import db, app  # Importation de db et app
from models import Reservation
from flask_migrate import Migrate
import random
import datetime
import locale

# Définir locale en français pour obtenir les jours correctement
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

# Initialisation de Flask-Migrate
migrate = Migrate(app, db)

# Horaires du restaurant
HORAIRES_RESTAURANT = {
    "lundi": [("12:00", "14:30"), ("19:00", "22:30")],
    "mardi": [("12:00", "14:30"), ("19:00", "22:30")],
    "mercredi": [("12:00", "14:30"), ("19:00", "22:30")],
    "jeudi": [("12:00", "14:30"), ("19:00", "22:30")],
    "vendredi": [("12:00", "14:30"), ("19:00", "22:30")],
    "samedi": [("12:00", "15:00"), ("19:00", "23:00")],
    "dimanche": []
}

TOTAL_COUVERTS_DISPONIBLES = 50

def obtenir_jour_semaine(date_str):
    """Retourne le jour de la semaine en français à partir d'une date (YYYY-MM-DD)."""
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A").lower()

@app.route('/horaires-disponibles', methods=['GET'])
def get_horaires_disponibles():
    """Retourne les créneaux disponibles pour une date donnée."""
    date = request.args.get('date')
    if not date:
        return jsonify({"message": "Date requise"}), 400
    
    jour = obtenir_jour_semaine(date)
    horaires = HORAIRES_RESTAURANT.get(jour, [])
    
    if not horaires:
        return jsonify({"message": "Le restaurant est fermé ce jour-là."}), 400
    
    disponibilites = []
    for debut, fin in horaires:
        heure_actuelle = datetime.datetime.strptime(debut, "%H:%M")
        fin_horaire = datetime.datetime.strptime(fin, "%H:%M")
        while heure_actuelle <= fin_horaire:
            heure_str = heure_actuelle.strftime("%H:%M")
            couverts_reserves = db.session.query(Reservation).filter_by(date=date, horaire=heure_str).all()
            total_reserves = sum(res.nombre_couverts for res in couverts_reserves)
            if total_reserves < TOTAL_COUVERTS_DISPONIBLES:
                disponibilites.append(heure_str)
            heure_actuelle += datetime.timedelta(minutes=30)
    
    return jsonify({"horaires_disponibles": disponibilites})

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
    
    jour = obtenir_jour_semaine(date)
    horaires_jour = HORAIRES_RESTAURANT.get(jour, [])

    # Générer tous les créneaux valides (30 min d'intervalle)
    horaires_valides = []
    for debut, fin in horaires_jour:
        heure_actuelle = datetime.datetime.strptime(debut, "%H:%M")
        fin_horaire = datetime.datetime.strptime(fin, "%H:%M")
        while heure_actuelle <= fin_horaire:
            horaires_valides.append(heure_actuelle.strftime("%H:%M"))
            heure_actuelle += datetime.timedelta(minutes=30)

    if horaire not in horaires_valides:
        return jsonify({"message": "Horaire non disponible"}), 400
    
    couverts_reserves = db.session.query(Reservation).filter_by(date=date, horaire=horaire).all()
    total_reserves = sum(res.nombre_couverts for res in couverts_reserves)
    
    if total_reserves + nombre_couverts > TOTAL_COUVERTS_DISPONIBLES:
        return jsonify({"message": "Nombre de couverts insuffisant pour cette date et cet horaire"}), 400
    
    nouveau_code = str(random.randint(1000, 9999))
    
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

if __name__ == '__main__':
    app.run(debug=True)
