from flask import Flask
from flask_cors import CORS

from routes.cart import add_to_cart
from routes.cart import get_cart

from routes.products import get_products

from routes.cart import remove_from_cart

from routes.orders import checkout

from routes.orders import get_orders


app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "AWS E-Commerce Backend Running"


@app.route("/products")
def products():

    return get_products()


@app.route("/cart/add", methods=["POST"])
def cart_add():
    return add_to_cart()


@app.route("/cart", methods=["GET"])
def cart_view():
    return get_cart()


@app.route("/cart/remove/<int:index>",methods=["DELETE"])
def cart_remove(index):
    return remove_from_cart(index)  


@app.route( "/checkout",methods=["POST"])
def order_checkout():
    return checkout()    


@app.route("/orders")
def orders():
    return get_orders()    

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )