# import importlib
# import os
#
# # Get all files.
# views = [
#     f
#     for f in os.listdir(os.path.dirname(os.path.abspath(__file__)))
#     if f.endswith(".py") and f != "__init__.py"
# ]
#
# # Import all files from modules folder.
# for view in views:
#     importlib.import_module(
#         os.path.dirname(os.path.realpath(__file__)).split("/")[-1] + "." + view[:-3]
#     )
#     print("App imported " + view + " successfully.")

# from flask import Blueprint
# from . import machine
# from .database import sqlite_service
# from .machine import api, errors, exception
#
# machine_blueprint = Blueprint('machines', __name__)
