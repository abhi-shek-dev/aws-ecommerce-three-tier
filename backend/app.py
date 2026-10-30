import logging
import os

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from routes.cart import bp as cart_bp
from routes.orders import bp as orders_bp
from routes.products import bp as products_bp

logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)

    # In AWS the browser talks to Nginx on the same origin (/api), so CORS only matters locally.
    origins = [
        o.strip()
        for o in os.environ.get(
            "CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000"
        ).split(",")
        if o.strip()
    ]
    CORS(app, origins=origins)

    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    @app.get("/")
    def home():
        return "AWS E-Commerce Backend Running"

    @app.get("/health")
    def health():
        # Used by the load balancer health checks. Deliberately does not touch the database.
        return jsonify({"status": "ok"})

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"message": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled error")
        return jsonify({"message": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    # Local development only. In AWS the app runs under gunicorn (see deploy/).
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
