from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/menu', methods=['GET'])
def get_menu():
    return "hello"

@app.route('/reserverTable', methods=['POST'])
def reserver_table():
    return "Bonjour"

@app.route('/placeOrder', methods=['POST'])
def commander():
    return "Hola"


@app.route('/cancelReservation', methods=['DELETE'])
def annuler_table():
    return "Salut"

@app.route('/modifyReservation', methods=['PUT'])
def modifier_table():
    return "Coucou"

@app.route('/cancelOrder', methods=['DELETE'])
def annuler_commande():
    return "CIao"

@app.route('/modifyOrder', methods=['PUT'])
def modifier_commande():
    return "Aurevoir"

if __name__ == '__main__':
    app.run(debug=True)
