from uuid import uuid4
from random import choice
from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth


# {id: {name, price}}
menu = {1: {"name": "Margherita", "price": 8.99},
          2: {"name": "Pepperoni", "price": 9.99}}

# {id: {status, total_price, name}}
orders = {}
statuses = ["ready_to_be_delivered", "not_ready_to_be_delivered"]

# name
users = []

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

ADMIN_TOKEN = "supersecrettoken"

@auth.verify_token
def verify_token(token):
    return token == ADMIN_TOKEN

@app.route("/menu", methods = ["GET"])
def get_menu():
    return jsonify(menu), 200

# request format:
# {"user": user, "order": [pizza_ids], "token": token}
@app.route("/order", methods = ["POST"])
def create_order():
    data = request.get_json()
    users.append(data["user"])

    order_id = str(uuid4())
    order = data["order"]

    print(data)

    total_price = 0
    for o in order:
        if o not in menu:
            return jsonify({"error": "One of the given items is not on the menu!"}), 404
        total_price += menu[o]["price"]

    status = choice(statuses)

    orders[order_id] = {"status": status, "total_price": total_price, "name": data["user"]}

    return {"order_id": order_id, "status": status, "total_price": total_price}, 201


@app.route("/order/<order_id>", methods = ["GET"])
def get_order_status(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found!"}), 404
    return jsonify({"status": orders[order_id]["status"]})


@app.route("/order/<order_id>", methods = ["DELETE"])
def cancel_order(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found!"}), 404
    
    if orders[order_id]["status"] == "not_ready_to_be_delivered":
        orders.pop(order_id)
        return jsonify({"message": f"Successfully deleted order {order_id}"}), 200
    else:
        return jsonify({"message": f"Order {order_id} already ready to be delivered!"}), 200
    

# request format:
# {"name": name, "price": price}
@app.route("/menu", methods = ["POST"])
@auth.login_required
def add_pizza_admin():
    data = request.json
    pizza_id = len(menu) + 1
    menu[pizza_id] = {"name": data["name"], "price": data["price"]}
    return jsonify({"message": "Pizza added", "pizza_id": pizza_id}), 201


@app.route("/menu/<pizza_id>", methods = ["DELETE"])
@auth.login_required
def delete_pizza_admin(pizza_id):
    pizza_id = int(pizza_id)
    if pizza_id not in menu:
        return jsonify({"error": "Pizza not found!"}), 404

    menu.pop(pizza_id)
    return jsonify({"message": f"Successfully deleted pizza {pizza_id}"}), 200


@app.route("/admin/order/<order_id>", methods = ["DELETE"])
@auth.login_required
def cancel_order_admin(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found!"}), 404
    
    orders.pop(order_id)
    return jsonify({"message": f"Successfully deleted order {order_id}"}), 200


if __name__ == "__main__":
    app.run(debug=True)