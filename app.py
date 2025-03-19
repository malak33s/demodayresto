from flask import Flask, jsonify, request
from db_connection import db, app  # Importation de db et app
from models import Reservation, Menu, Commande
from flask_migrate import Migrate
import random
import datetime
import locale
import uuid # Pour générer des codes de réservation uniques


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
        while heure_actuelle < fin_horaire:  # Correction ici
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

    try:
        nombre_couverts = int(nombre_couverts)
    except ValueError:
        return jsonify({"message": "Nombre de couverts doit être un entier"}), 400
    
    if nombre_couverts <= 0:
        return jsonify({"message": "Nombre de couverts invalide"}), 400

    jour = obtenir_jour_semaine(date)
    
    # Vérifier si c'est dimanche
    if jour.lower() == "dimanche":
        return jsonify({"message": "Restaurant fermé"}), 400

    horaires_jour = HORAIRES_RESTAURANT.get(jour, [])

    horaires_valides = []
    for debut, fin in horaires_jour:
        heure_actuelle = datetime.datetime.strptime(debut, "%H:%M")
        fin_horaire = datetime.datetime.strptime(fin, "%H:%M")
        while heure_actuelle < fin_horaire:
            horaires_valides.append(heure_actuelle.strftime("%H:%M"))
            heure_actuelle += datetime.timedelta(minutes=1)

    # Vérifier si l'horaire est disponible
    if horaire not in horaires_valides:
        return jsonify({"message": "Horaire indisponible"}), 400

    couverts_reserves = db.session.query(Reservation).filter_by(date=date, horaire=horaire).all()
    total_reserves = sum(res.nombre_couverts for res in couverts_reserves)
    
    if total_reserves + nombre_couverts > TOTAL_COUVERTS_DISPONIBLES:
        return jsonify({"message": "Nombre de couverts non disponible"}), 400
    
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


@app.route('/ajouter-menus', methods=['POST'])
def ajouter_menus():
    """ menus à la base de données."""
    plats = [
        {"nom": "Brick", "description": "Brick garnie d'un œuf coulant, de thon, de persil et d'épices.",
         "type": "entrée", "prix": 2.90, "quantite_disponible": 30, "temps_preparation": 20},
        {"nom": "Riz Djerbien", "description": "Riz parfumé aux épices, accompagné de viande de veau.",
         "type": "plat", "prix": 12.00, "quantite_disponible": 30, "temps_preparation": 30},
        {"nom": "Baklawa", "description": "Feuilles de pâte fine, noix et miel.",
         "type": "dessert", "prix": 3.00, "quantite_disponible": 30, "temps_preparation": 10},
        {"nom": "Ice tea pêche", "description": "Ice tea goût pêche (33cl).",
         "type": "boisson", "prix": 2.00, "quantite_disponible": 50, "temps_preparation": 2}
    ]

    for plat in plats:
        if not Menu.query.filter_by(nom=plat["nom"]).first():
            nouveau_plat = Menu(**plat)
            db.session.add(nouveau_plat)

    db.session.commit()
    return jsonify({"message": "Menus ajoutés"}), 201

@app.route('/menus', methods=['GET'])
def get_menus():
    """Retourne tous les plats disponibles avec leurs détails."""
    menus = Menu.query.all()
    result = [
        {
            "nom": menu.nom,
            "description": menu.description,
            "type": menu.type,
            "prix": menu.prix,
            "quantite_disponible": menu.quantite_disponible,
            "temps_preparation": menu.temps_preparation
        }
        for menu in menus
    ]
    return jsonify(result), 200

#PARTIE ADMIN - GESTION DES RÉSERVATIONS
# Route pour obtenir toutes les réservations
@app.route('/admin/reservations', methods=['GET'])
def obt_reservations():
    reservations = Reservation.query.all()
    result = [
        {
            "id": reservation.id,
            "nom": reservation.nom,
            "date": reservation.date if reservation.date else None,
            "horaire": reservation.horaire,
            "nombre_couverts": reservation.nombre_couverts,
            "code_reservation": reservation.code_reservation
        }
        for reservation in reservations
        ]
    return jsonify(result), 200

# Récupérer une réservation par l'ID
@app.route('/admin/reservations/<int:reservation_id>', methods=['GET'])
def recup_reservation_par_id(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"message": "Réservation introuvable"}), 404
    
    result = {
        "id": reservation.id,
        "nom": reservation.nom,
        "date": reservation.date if reservation.date else None,
        "horaire": reservation.horaire,
        "nombre_couverts": reservation.nombre_couverts,
        "code_reservation": reservation.code_reservation
        }
    return jsonify(result), 200

# Ajouter une réservation côté admin
@app.route('/admin/reservations', methods=['POST'])
def ajout_reservation_admin():
    try:
        data = request.get_json()
        nom = data.get('nom')
        date = data.get('date')
        horaire = data.get('horaire')
        nombre_couverts = data.get('nombre_couverts')
        
        if not all([nom, date, horaire, nombre_couverts]):
            db.session.rollback()
            return jsonify({"message": "Tous les champs doivent être remplis"}), 400
        
        # Génération du code unique
        code_reservation = str(uuid.uuid4())[:8]
        nouvelle_reservation = Reservation(
            nom=nom,
            date=date,
            horaire=horaire,
            nombre_couverts=nombre_couverts,
            code_reservation=code_reservation
            )
        
        db.session.add(nouvelle_reservation)
        db.session.commit()
        return jsonify({"message": "Réservation ajoutée côté admin", "code_reservation": code_reservation}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Route pour supprimer une réservation
@app.route('/admin/reservations/<int:id>', methods=['DELETE'])
def supp_reservation(id):
    try:
        reservation = Reservation.query.get(id)
        if not reservation:
            return jsonify({"message": "Réservation introuvable"}), 404
        
        db.session.delete(reservation)
        db.session.commit() # mise à jour bd
        return jsonify({"message": "Réservation supprimée"}), 200
    except Exception as e: # si rien fonctionne
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Route pour modifier une réservation
@app.route('/admin/reservations/<int:id>', methods=['PUT'])
def modifier_reservation(id):
    try:
        reservation = Reservation.query.get(id)
        if not reservation:
            return jsonify({"message": "Réservation introuvable"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "Données invalides"}), 400
        
        # Mise à jour pour les champs
        reservation.nom = data.get("nom", reservation.nom)
        reservation.date = data.get("date", reservation.date)
        reservation.horaire = data.get("horaire", reservation.horaire)
        
        nombre_couverts = data.get("nombre_couverts")
        if nombre_couverts is not None:
            try:
                nombre_couverts = int(nombre_couverts)
                if nombre_couverts <= 0:
                    return jsonify({"message": "Nombre de couverts invalide"}), 400
                reservation.nombre_couverts = nombre_couverts
            except ValueError:
                return jsonify({"message": "Nombre de couverts doit être un nombre entier"}), 400
            
            db.session.commit()
            return jsonify({"message": "Réservation modifiée"}), 200
    except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Erreur lors de la modification de la réservation", "error": str(e)}), 500

#PARTIE ADMIN
# Route pour obtenir toutes les commandes
@app.route('/admin/commandes', methods=['GET'])
def obt_commandes():
    commandes = Commande.query.all()
    result=[
        {
            "id": commande.id,
            "nom_client": commande.nom_client,
            "plats": commande.plats,
            "heure_retrait": commande.heure_retrait,
            "statut": commande.statut,
            "code_reservation": commande.code_reservation,
            "created_at": commande.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for commande in commandes
    ]
    return jsonify(result), 200

# Récupérer une commande par l'ID
@app.route('/admin/commandes/<int:commande_id>', methods=['GET'])
def recup_commande_par_id(commande_id):
    commande = Commande.query.get(commande_id)
    if not commande:
        return jsonify({"message": "Commande introuvable"}), 404
    else:
        result = {
                "id": commande.id,
                "nom_client": commande.nom_client,
                "plats": commande.plats,
                "heure_retrait": commande.heure_retrait,
                "statut": commande.statut,
                "code_reservation": commande.code_reservation,
                "created_at": commande.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify(result), 200

# Ajouter une commande coté admin
@app.route('/admin/commandes', methods=['POST'])
def ajout_commande_admin():
    try:
        data = request.get_json()
        nom_client = data.get('nom_client')
        date = data.get('date')
        plats = data.get('plats')
        total = data.get('total')
        
        if not all([nom_client, date, plats, total]):
            return jsonify({"message": "Tous les champs doivent être remplis"}), 400
        
        code_commande = str(uuid.uuid4())[:8]
        nouvelle_commande = Commande(
            nom_client=nom_client,
            date=date,
            plats=plats,
            total=total,
            code_commande=code_commande
)

        
        db.session.add(nouvelle_commande)
        db.session.commit()
        return jsonify({"message": "Commande ajoutée coté admin", "code_commande": code_commande}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erreur lors de l'ajout de la commande", "error": str(e)}), 500

# Route pour supprimer une commande
@app.route('/admin/commandes/<int:id>', methods=['DELETE'])
def supp_commande(id):
    try:
        commande = Commande.query.get(id)
        
        if not commande:
            return jsonify({"message": "Commande introuvable"}), 404

        db.session.delete(commande)
        db.session.commit()
        return jsonify({"message": "Commande supprimée"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erreur lors de la suppression de la commande", "error": str(e)}), 500

# Route pour modifier une commande
@app.route('/admin/commandes/<int:id>', methods=['PUT'])
def modifier_commande(id):
    try:
        commande = commande.query.get(id)
        if not commande:
            return jsonify({"message": "Commande introuvable"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"message": "Données invalides"}), 400

        commande.nom_client = data.get("nom_client", commande.nom_client)
        commande.date = data.get("date", commande.date)
        commande.plats = data.get("plats", commande.plats)
        commande.total = data.get("total", commande.total)

        db.session.commit()
        return jsonify({"message": "Commande modifiée"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erreur lors de la modification de la commande", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)