from flask import jsonify
from modules.machine import machine_blueprint
from modules.machine.exception import StocksCaculateError


@machine_blueprint.errorhandler(400)
def handle_error_400(e):
    return "400, bad request.", 400


@machine_blueprint.errorhandler(404)
def handle_error_404(e):
    return "404, page not found.", 404


@machine_blueprint.errorhandler(405)
def handle_error_405(e):
    return "405, HTTP method not allowed.", 405


@machine_blueprint.errorhandler(408)
def handle_error_408(e):
    return "408, your request is taking too long to be served.}", 408


@machine_blueprint.errorhandler(StocksCaculateError)
def handle_stock_error(e):
    status_code = 500
    success = False
    response = {
        "success": success,
        "error": {
            "type": "NegativeStockException",
            "message": "The stock is insufficient",
        },
    }

    return jsonify(response), status_code
