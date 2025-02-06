from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/menu', methods=['GET'])
def get_menu():
    return "Voir Menu"

@app.route('/reserverTable', methods=['POST'])
def reserver_table():
    return "Bonjour je voudrais réserver une table"

@app.route('/placeOrder', methods=['POST'])
def commander():
    return "Je voudrais ce plat svp"


@app.route('/cancelReservation', methods=['DELETE'])
def annuler_table():
    return "Bonjour je voudrais annuler cette réservation"

@app.route('/modifyReservation', methods=['PUT'])
def modifier_table():
    return "Bonjour je voudrais modifier cette réservation"

@app.route('/cancelOrder', methods=['DELETE'])
def annuler_commande():
    return "annulation commande"

@app.route('/modifyOrder', methods=['PUT'])
def modifier_commande():
    return "modification commande"

if __name__ == '__main__':
    app.run(debug=True)
