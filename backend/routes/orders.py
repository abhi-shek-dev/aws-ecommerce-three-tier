from flask import jsonify
from config import cursor, db


def checkout():

    cursor.execute(
        """
        SELECT *
        FROM cart
        """
    )

    cart_items = cursor.fetchall()

    if not cart_items:

        return jsonify(
            {
                "message": "Cart is empty"
            }
        )

    total = 0

    for item in cart_items:

        total += (
            float(item["price"])
            * item["quantity"]
        )

    cursor.execute(
        """
        INSERT INTO orders
        (
            total_amount
        )
        VALUES
        (
            %s
        )
        """,
        (total,)
    )

    cursor.execute(
        """
        DELETE FROM cart
        """
    )

    db.commit()

    return jsonify(
        {
            "message":
                "Order placed successfully",

            "total":
                total
        }
    )


def get_orders():

    cursor.execute(
        """
        SELECT *
        FROM orders
        ORDER BY id DESC
        """
    )

    orders = cursor.fetchall()

    return jsonify(orders)    