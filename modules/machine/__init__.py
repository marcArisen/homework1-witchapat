from flask import Blueprint

machine_blueprint = Blueprint("machines", __name__)

from . import api, errors, exception
