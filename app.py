# Import Libraries 
from flask import Flask, jsonify, request

from machine import Machine
from sqlite_service import *

# Define app.
app = Flask(__name__)

@app.route('/machine/<uuid>', methods=['POST'])
def create_machine(uuid):
    req = request.json
    machine = Machine(name=req['name'], location=['location'] )
    
    return jsonify({"uuid":uuid})