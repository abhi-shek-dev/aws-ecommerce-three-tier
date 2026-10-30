from flask import Blueprint, jsonify

from config import db_cursor

bp = Blueprint("products", __name__)


@bp.get("/products")
def list_products():
    with db_cursor() as cursor:
        cursor.execute("SELECT id, name, price FROM products ORDER BY id")
        rows = cursor.fetchall()

    return jsonify([{"id": r["id"], "name": r["name"], "price": float(r["price"])} for r in rows])
