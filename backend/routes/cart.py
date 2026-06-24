from flask import request, jsonify

from config import cursor, db

cart = []


def add_to_cart():

    data = request.json

    cursor.execute(
        """
        SELECT *
        FROM cart
        WHERE product_name = %s
        """,
        (data["name"],)
    )

    existing_item = cursor.fetchone()

    if existing_item:

        cursor.execute(
            """
            UPDATE cart
            SET quantity = quantity + 1
            WHERE product_name = %s
            """,
            (data["name"],)
        )

    else:

        cursor.execute(
            """
            INSERT INTO cart
            (
                product_name,
                price,
                quantity
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                data["name"],
                data["price"],
                1
            )
        )

    db.commit()

    return jsonify(
        {
            "message": "Item added"
        }
    )


def get_cart():

    cursor.execute(
        """
        SELECT *
        FROM cart
        """
    )

    cart_items = cursor.fetchall()

    return jsonify(cart_items)


def remove_from_cart(index):

    cursor.execute(
        """
        DELETE FROM cart
        WHERE id = %s
        """,
        (index,)
    )

    db.commit()

    return jsonify(
        {
            "message": "Item removed"
        }
    )