from flask import jsonify
from config import cursor


def get_products():

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    return jsonify(products)