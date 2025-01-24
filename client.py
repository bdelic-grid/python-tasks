import argparse
import requests
import sys
import json

server_url = "http://localhost:5000"

def send_request(endpoint, method, data=None, token=None):
    url = server_url + endpoint
    headers = {}

    if token is not None:
        headers = {"Authorization": f"Bearer {token}"}

    if method == "GET":
        res = requests.get(url, headers=headers)
    elif method == "POST":
        res = requests.post(url, headers=headers, json=data)
    elif method == "DELETE":
        res = requests.delete(url, headers=headers)
    else:
        print("Invalid request, send only GET, POST, DELETE are allowed!")
        sys.exit(1)

    if res.status_code == 401:
        print("Unauthorized, invalid token!")
        sys.exit(1)
    else:
        print(res.text)


def list_menu():
    send_request("/menu", method = "GET")


def create_order(orders, username):
    payload = {
        "user": username,
        "order": [item for item in orders.split(',')]
    }
    payload = json.dumps(payload)
    send_request("/order", method="POST", data=payload)


def check_status(id):
    send_request(f"/order/{id}", method="GET")


def cancel_order(id):
    send_request(f"/order/{id}", method="DELETE")


def add_pizza_admin(name, price, token):
    payload = {
        "name": name,
        "price": price
    }
    send_request(f"/menu", method="POST", data=payload, token=token)

def delete_pizza_admin(id, token):
    send_request(f"/menu/{id}", method="DELETE", token=token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pizza ordering CLI")

    parser.add_argument("role", choices=["customer", "admin"], help="Specify the role")
    parser.add_argument("request", choices=["list_menu", "create_order", "check_status", "cancel_order", "add_pizza_admin", "delete_pizza_admin", "cancel_order_admin"])

    parser.add_argument("--pizza_ids", type=str, help="Pizza IDs for order creation")
    parser.add_argument("--username", type=str, help="Username for order creation")
    parser.add_argument("--order_id", type=str, help="Order ID for checking order status/deleting it")

    parser.add_argument("--name", type=str, help="Name of new pizza")
    parser.add_argument("--price", type=str, help="Price of new pizza")
    parser.add_argument("--token", type=str, help="Admin token")

    args = parser.parse_args()

    if args.role == "customer":
        if args.request == "list_menu":
            list_menu()

        elif args.request == "create_order":
            if not args.pizza_ids:
                print("Pizza IDs are required to make an order!")
                sys.exit(1)
            if not args.username:
                print("Username is required to make an order!")
                sys.exit(1)
            create_order(args.pizza_ids, args.username)

        elif args.request == "check_status":
            if not args.order_id:
                print("Order ID is required to check its status!")
                sys.exit(1)
            check_status(args.order_id)

        elif args.request == "cancel_order":
            if not args.order_id:
                print("Order ID is required to cancel it!")
                sys.exit(1)
            cancel_order(args.order_id)
        
    elif args.role == "admin":
        if not args.token:
            print("Please provide an admin token!")
            sys.exit(1)

        if args.request == "add_pizza_admin":
            if not args.name or not args.price:
                print("Pizza name and/or price missing!")
                sys.exit(1)
            elif not args.token:
                print("Provide an admin token!")
                sys.exit(1)
            add_pizza_admin(args.name, args.price, args.token)

        if args.request == "delete_pizza_admin":
            if not args.pizza_ids:
                print("Provide pizza id!")
                sys.exit(1)
            elif not args.token:
                print("Provide an admin token!")
                sys.exit(1)
            delete_pizza_admin(args.pizza_ids, args.token)

    else:
        print("Invalid role! Choose either admin or customer")