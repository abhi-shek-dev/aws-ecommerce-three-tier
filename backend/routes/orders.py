from flask import Blueprint, abort, jsonify

from config import db_cursor
from routes.common import get_client_id

bp = Blueprint("orders", __name__)


@bp.post("/checkout")
def checkout():
    client_id = get_client_id()

    with db_cursor() as cursor:
        # FOR UPDATE serialises double-submits: a second checkout waits, then finds an empty cart.
        cursor.execute(
            """
            SELECT c.product_id, c.quantity, p.price
            FROM cart c
            JOIN products p ON p.id = c.product_id
            WHERE c.client_id = %s
            FOR UPDATE OF c
            """,
            (client_id,),
        )
        items = cursor.fetchall()

        if not items:
            abort(400, description="Cart is empty")

        total = sum(row["price"] * row["quantity"] for row in items)  # Decimal maths, not float

        cursor.execute(
            "INSERT INTO orders (client_id, total_amount) VALUES (%s, %s)",
            (client_id, total),
        )
        order_id = cursor.lastrowid

        cursor.executemany(
            """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            """,
            [(order_id, r["product_id"], r["quantity"], r["price"]) for r in items],
        )

        cursor.execute("DELETE FROM cart WHERE client_id = %s", (client_id,))

    return (
        jsonify(
            {
                "message": "Order placed successfully",
                "order_id": order_id,
                "total": float(total),
            }
        ),
        201,
    )


@bp.get("/orders")
def list_orders():
    client_id = get_client_id()

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, total_amount, order_date
            FROM orders
            WHERE client_id = %s
            ORDER BY id DESC
            """,
            (client_id,),
        )
        rows = cursor.fetchall()

    return jsonify(
        [
            {
                "id": r["id"],
                "total_amount": float(r["total_amount"]),
                "order_date": r["order_date"].isoformat(),
            }
            for r in rows
        ]
    )
