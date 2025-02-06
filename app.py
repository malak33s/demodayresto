from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données (utilisation de SQLite pour simplifier)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Définition des modèles

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    nombre_personnes = db.Column(db.Integer, nullable=False)
    numero_table = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Reservation('{self.id}', '{self.nom}', '{self.date}', '{self.nombre_personnes}', '{self.numero_table}')"

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_plat = db.Column(db.String(100), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    numero_table = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Commande('{self.id}', '{self.nom_plat}', '{self.quantite}', '{self.numero_table}')"

# Créer les tables dans la base de données
with app.app_context():
    db.create_all()

# Routes de l'API

@app.route('/menu', methods=['GET'])
def obtenir_menu():
    menu = [
        {"id": 1, "nom": "Couscous", "prix": 10.0},
        {"id": 2, "nom": "Brik", "prix": 5.0},
        {"id": 3, "nom": "Pâtisserie", "prix": 3.0}
    ]
    return jsonify(menu)

@app.route('/reserverTable', methods=['POST'])
def reserver_table():
    data = request.get_json()  # Récupère les données envoyées en JSON

    # Récupérer les informations du body de la requête
    nom = data.get('nom')
    date = data.get('date')
    nombre_personnes = data.get('nombre_personnes')
    numero_table = data.get('numero_table')

    # Créer une nouvelle réservation
    nouvelle_reservation = Reservation(
        nom=nom,
        date=date,
        nombre_personnes=nombre_personnes,
        numero_table=numero_table
    )

    # Ajouter et valider la réservation
    db.session.add(nouvelle_reservation)
    db.session.commit()

    return jsonify({"message": "Réservation ajoutée avec succès !"}), 201

@app.route('/commander', methods=['POST'])
def passer_commande():
    data = request.get_json()  # Récupère les données envoyées en JSON

    # Récupérer les informations du body de la requête
    nom_plat = data.get('nom_plat')
    quantite = data.get('quantite')
    numero_table = data.get('numero_table')

    # Créer une nouvelle commande
    nouvelle_commande = Commande(
        nom_plat=nom_plat,
        quantite=quantite,
        numero_table=numero_table
    )

    # Ajouter et valider la commande
    db.session.add(nouvelle_commande)
    db.session.commit()

    return jsonify({"message": "Commande ajoutée avec succès !"}), 201

@app.route('/annulerReservation', methods=['DELETE'])
def annuler_reservation():
    data = request.get_json()
    reservation_id = data.get('id')

    reservation = Reservation.query.get(reservation_id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": "Réservation annulée avec succès !"}), 200
    else:
        return jsonify({"message": "Réservation non trouvée"}), 404

@app.route('/modifierReservation', methods=['PUT'])
def modifier_reservation():
    data = request.get_json()
    reservation_id = data.get('id')
    nouvelle_date = data.get('date')
    nouveau_nombre_personnes = data.get('nombre_personnes')
    nouveau_numero_table = data.get('numero_table')

    reservation = Reservation.query.get(reservation_id)
    if reservation:
        reservation.date = nouvelle_date
        reservation.nombre_personnes = nouveau_nombre_personnes
        reservation.numero_table = nouveau_numero_table
        db.session.commit()
        return jsonify({"message": "Réservation modifiée avec succès !"}), 200
    else:
        return jsonify({"message": "Réservation non trouvée"}), 404

@app.route('/annulerCommande', methods=['DELETE'])
def annuler_commande():
    data = request.get_json()
    commande_id = data.get('id')

    commande = Commande.query.get(commande_id)
    if commande:
        db.session.delete(commande)
        db.session.commit()
        return jsonify({"message": "Commande annulée avec succès !"}), 200
    else:
        return jsonify({"message": "Commande non trouvée"}), 404

@app.route('/modifierCommande', methods=['PUT'])
def modifier_commande():
    data = request.get_json()
    commande_id = data.get('id')
    nouveau_nom_plat = data.get('nom_plat')
    nouvelle_quantite = data.get('quantite')
    nouveau_numero_table = data.get('numero_table')

    commande = Commande.query.get(commande_id)
    if commande:
        commande.nom_plat = nouveau_nom_plat
        commande.quantite = nouvelle_quantite
        commande.numero_table = nouveau_numero_table
        db.session.commit()
        return jsonify({"message": "Commande modifiée avec succès !"}), 200
    else:
        return jsonify({"message": "Commande non trouvée"}), 404

if __name__ == '__main__':
    app.run(debug=True)
