from flask import Flask
from modules.machine import machine_blueprint


# app = Flask(__name__)

# import modules

def create_app():
    app = Flask(__name__)
    app.register_blueprint(machine_blueprint)
    return app
