from flask import jsonify

from app import app
from modules.exception import StocksCaculateError


@app.errorhandler(400)
def handle_error_400(e):
    return "400, bad request.", 400


@app.errorhandler(404)
def handle_error_404(e):
    return "404, page not found.", 404


@app.errorhandler(405)
def handle_error_405(e):
    return "405, HTTP method not allowed.", 405


@app.errorhandler(408)
def handle_error_408(e):
    return "408, your request is taking too long to be served.}", 408


@app.errorhandler(StocksCaculateError)
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
