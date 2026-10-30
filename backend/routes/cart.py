from flask import Blueprint, abort, jsonify, request

from config import db_cursor
from routes.common import get_client_id

bp = Blueprint("cart", __name__)

MAX_QUANTITY = 10


@bp.get("/cart")
def view_cart():
    client_id = get_client_id()

    with db_cursor() as cursor:
        # The price always comes from the products table, never from the browser.
        cursor.execute(
            """
            SELECT c.id, p.name, p.price, c.quantity
            FROM cart c
            JOIN products p ON p.id = c.product_id
            WHERE c.client_id = %s
            ORDER BY c.id
            """,
            (client_id,),
        )
        rows = cursor.fetchall()

    return jsonify(
        [
            {
                "id": r["id"],
                "name": r["name"],
                "price": float(r["price"]),
                "quantity": r["quantity"],
            }
            for r in rows
        ]
    )


@bp.post("/cart/add")
def add_to_cart():
    client_id = get_client_id()
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")

    if not isinstance(product_id, int) or isinstance(product_id, bool):
        abort(400, description="product_id must be an integer")

    with db_cursor() as cursor:
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if cursor.fetchone() is None:
            abort(404, description="Product not found")

        # Atomic upsert: no read-then-write race when two clicks arrive together.
        cursor.execute(
            """
            INSERT INTO cart (client_id, product_id, quantity)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE quantity = LEAST(quantity + 1, %s)
            """,
            (client_id, product_id, MAX_QUANTITY),
        )

    return jsonify({"message": "Item added"})


@bp.delete("/cart/remove/<int:item_id>")
def remove_from_cart(item_id):
    client_id = get_client_id()

    with db_cursor() as cursor:
        # Scoped to the caller's own cart, so one visitor cannot delete another's items.
        cursor.execute(
            "DELETE FROM cart WHERE id = %s AND client_id = %s",
            (item_id, client_id),
        )
        if cursor.rowcount == 0:
            abort(404, description="Item not found in your cart")

    return jsonify({"message": "Item removed"})
