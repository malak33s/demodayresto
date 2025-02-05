from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://demodayresto:mot_de_passe@localhost/demoday_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Définition du modèle pour les restaurants
class Resto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

# Définition du modèle pour les commandes
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Définition du modèle pour les réservations
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)

# Création des tables dans la base de données
with app.app_context():
    db.create_all()

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({"message": "Liste des plats (à implémenter)"})

@app.route('/reserverTable', methods=['POST'])
def reserver_table():
    data = request.get_json()
    new_reservation = Reservation(customer_name=data['customer_name'], date=data['date'], time=data['time'])
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify({"message": "Table réservée avec succès !"})

@app.route('/placeOrder', methods=['POST'])
def commander():
    data = request.get_json()
    new_order = Order(dish_name=data['dish_name'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Commande passée avec succès !"})

@app.route('/cancelReservation/<int:id>', methods=['DELETE'])
def annuler_table(id):
    reservation = Reservation.query.get(id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"message": "Réservation annulée avec succès !"})
    return jsonify({"error": "Réservation non trouvée"}), 404

@app.route('/modifyReservation/<int:id>', methods=['PUT'])
def modifier_table(id):
    data = request.get_json()
    reservation = Reservation.query.get(id)
    if reservation:
        reservation.date = data.get('date', reservation.date)
        reservation.time = data.get('time', reservation.time)
        db.session.commit()
        return jsonify({"message": "Réservation modifiée avec succès !"})
    return jsonify({"error": "Réservation non trouvée"}), 404

@app.route('/cancelOrder/<int:id>', methods=['DELETE'])
def annuler_commande(id):
    order = Order.query.get(id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Commande annulée avec succès !"})
    return jsonify({"error": "Commande non trouvée"}), 404

@app.route('/modifyOrder/<int:id>', methods=['PUT'])
def modifier_commande(id):
    data = request.get_json()
    order = Order.query.get(id)
    if order:
        order.quantity = data.get('quantity', order.quantity)
        db.session.commit()
        return jsonify({"message": "Commande modifiée avec succès !"})
    return jsonify({"error": "Commande non trouvée"}), 404

if __name__ == '__main__':
    app.run(debug=True)
