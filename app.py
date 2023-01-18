# Import Libraries 
from flask import Flask, jsonify, request
# import modules
from modules.exception import StocksCaculateError

from modules.machine import Machine
from modules.sqlite_service import *

# Define app.
db = Database_Service()
app = Flask(__name__)


@app.route('/machines', methods=['POST'])
def create_machine():
    req = request.json
    machine = Machine(name=req['name'], location=req['location'] )
    db.insert_into_machine(machine)
    return jsonify()

@app.route('/machines', methods=['GET'])
def get_all_machine():
    return jsonify(db.get_all())

@app.route('/machines/<uuid>', methods=['GET'])
def get_machine_by_id(uuid):
    return jsonify(db.get_by_id(uuid))

@app.route('/machines/<uuid>', methods=['POST'])
def update_stock(uuid):
    machine = db.get_by_id(uuid)
    stock = machine[stock]
    
    db.insert_into_machine(machine)
    return jsonify()

@app.route('/error', methods=['GET'])
def test_error_handle():
    i = 0
    raise StocksCaculateError
    return jsonify()