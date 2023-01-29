from flask import Flask, jsonify, request
# import modules
from modules.exception import StocksCaculateError
from app import app
from modules.machine import Machine
from modules.sqlite_service import *


@app.route('/machines', methods=['POST'])
def create_machine():
    req = request.json
    machine = Machine(name=req['name'], location=req['location'])
    inserted_id = db.insert_into_machine(machine)
    return jsonify(db.get_by_id(str(inserted_id)))


@app.route('/machines', methods=['GET'])
def get_all_machine():
    return jsonify(db.get_all_machines())


@app.route('/machines/<uuid>', methods=['GET'])
def get_machine_by_id(uuid):
    return jsonify(db.get_by_id(uuid))


@app.route('/machines/<uuid>', methods=['PUT'])
def add_stock_by_json(uuid):
    machine = db.get_by_id(uuid)
    stock = machine["stock"]
    to_add = request.json
    to_update = {}
    for item in to_add:
        if item in stock:
            added_amount = stock[item] + to_add[item]
            to_update[item] = added_amount
        else:
            to_update[item] = to_add[item]

    db.update_stock(uuid, to_update)
    return db.get_by_id(uuid)


@app.route('/machines/<uuid>', methods=['POST'])
def delete_stock_by_json(uuid):
    machine = db.get_by_id(uuid)
    stock = machine["stock"]
    to_remove = request.json
    to_update = {}

    for item in to_remove:
        amount_to_remove = to_remove[item]
        if item in stock and amount_to_remove <= stock[item]:
            leftover_amount = stock[item] - amount_to_remove
            if leftover_amount > 0:
                to_update[item] = stock[item] - amount_to_remove
        else:
            raise StocksCaculateError

    db.update_stock(uuid, to_update)
    return db.get_by_id(uuid)


@app.route('/machines/<uuid>', methods=['DELETE'])
def delete_machine(uuid):
    db.delete_machine(uuid)
    return "id '%s' already deleted!" % uuid, 200
