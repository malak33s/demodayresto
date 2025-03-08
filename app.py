from flask import Flask, jsonify, request
from db_connection import db, app  # Importation de db et app
from models import Reservation, Menu, Commande, CommandeItem  # Importation groupée
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

def verifier_heure_retrait(date_retrait, heure_retrait):
    """Vérifie si l'heure de retrait est dans les horaires d'ouverture du restaurant."""
    jour = obtenir_jour_semaine(date_retrait)
    horaires_jour = HORAIRES_RESTAURANT.get(jour, [])
    
    # Vérifie si le restaurant est ouvert ce jour-là
    if not horaires_jour:
        return False
    
    # Vérifie si l'heure de retrait est dans l'un des créneaux horaires du jour
    for debut, fin in horaires_jour:
        heure_debut = datetime.datetime.strptime(debut, "%H:%M")
        heure_fin = datetime.datetime.strptime(fin, "%H:%M")
        heure_retrait_obj = datetime.datetime.strptime(heure_retrait, "%H:%M")
        
        # Si l'heure de retrait est dans les horaires
        if heure_debut <= heure_retrait_obj <= heure_fin:
            return True
    
    return False

TOTAL_COUVERTS_DISPONIBLES = 50

def obtenir_jour_semaine(date_str):
    """Retourne le jour de la semaine en français à partir d'une date (YYYY-MM-DD)."""
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A").lower()

@app.route('/')
def home():
    """Route pour la page d'accueil"""
    return "Bienvenue sur le site du restaurant!"

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
        while heure_actuelle < fin_horaire:
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
    horaires_jour = HORAIRES_RESTAURANT.get(jour, [])

    horaires_valides = []
    for debut, fin in horaires_jour:
        heure_actuelle = datetime.datetime.strptime(debut, "%H:%M")
        fin_horaire = datetime.datetime.strptime(fin, "%H:%M")
        while heure_actuelle < fin_horaire:
            horaires_valides.append(heure_actuelle.strftime("%H:%M"))
            heure_actuelle += datetime.timedelta(minutes=1)

    if horaire not in horaires_valides:
        return jsonify({"message": "Horaires indisponibles"}), 400
    
    # Vérifier la disponibilité des couverts
    couverts_reserves = db.session.query(Reservation).filter_by(date=date, horaire=horaire).all()
    total_reserves = sum(res.nombre_couverts for res in couverts_reserves)
    
    if total_reserves + nombre_couverts > TOTAL_COUVERTS_DISPONIBLES:
        return jsonify({"message": "Nombre de couverts non disponible"}), 400
    
    # Générer un code de réservation unique
    nouveau_code = str(random.randint(1000, 9999))
    
    # Créer une nouvelle réservation
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
    """Menus à la base de données."""
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

@app.route('/api/commande', methods=['POST'])
def create_commande():
    """Créer une commande à emporter."""
    data = request.get_json()

    nom_client = data.get('name')
    date_retrait = data.get('date')
    heure_retrait = data.get('time')
    items = data.get('items')  # Liste des articles dans la commande

    if not nom_client or not date_retrait or not heure_retrait or not items:
        return jsonify({"message": "Tous les champs sont requis (nom, date, heure, articles)"}), 400

    # Validation de l'heure de retrait
    if not verifier_heure_retrait(date_retrait, heure_retrait):
        return jsonify({"message": "L'heure de retrait est en dehors des horaires d'ouverture du restaurant."}), 400

    # Calculer le total de la commande
    total = sum(item['price'] * item['quantity'] for item in items)

    # Créer une nouvelle commande dans la base de données
    nouvelle_commande = Commande(
        nom_client=nom_client,
        date_retrait=date_retrait,
        heure_retrait=heure_retrait,
        total=total,
        statut="En attente",  # Statut initial
    )

    db.session.add(nouvelle_commande)
    db.session.commit()

    # Ajouter les articles de la commande dans une table liée (CommandeItem)
    for item in items:
        commande_item = CommandeItem(
            commande_id=nouvelle_commande.id,
            plat_id=item['id'],
            quantite=item['quantity'],
            prix_total=item['price'] * item['quantity']
        )
        db.session.add(commande_item)

    db.session.commit()

    return jsonify({
        "message": "Commande enregistrée",
        "order_id": nouvelle_commande.id,
        "nom_client": nom_client,
        "date_retrait": date_retrait,
        "heure_retrait": heure_retrait,
        "total": total,
        "items": items
    }), 201


@app.route('/commandes/<int:id>', methods=['GET'])
def get_commande(id):
    """Retourne les détails d'une commande par son ID."""
    commande = Commande.query.get(id)
    if not commande:
        return jsonify({"message": "Commande non trouvée"}), 404
    
    return jsonify({
        "id": commande.id,
        "nom_client": commande.nom_client,
        "plats": [{"nom": item.plat.nom, "quantite": item.quantite, "prix": item.prix_total} for item in commande.items],
        "heure_retrait": commande.heure_retrait,
        "total": commande.total,
        "statut": commande.statut
    }), 200

@app.route('/commandes/<int:id>/confirmer', methods=['POST'])
def confirmer_commande(id):
    """Confirmer la commande finale."""
    commande = Commande.query.get(id)
    if not commande:
        return jsonify({"message": "Commande non trouvée"}), 404

    commande.statut = "Confirmée"
    db.session.commit()

    return jsonify({"message": "Commande confirmée"}), 200

if __name__ == '__main__':
    app.run(debug=True)
