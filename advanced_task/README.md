# Instructions to run

To start server, run: `python3 server.py`.

General approach to run client is: `python3 client.py <user_role> <action> [arguments]`
User role can be either admin or customer. **If you are acting as an admin, please provide the `--token` argument with the value `supersecrettoken`.**

## Available actions
### For customers
- list_menu
  
  Lists the available pizzas on the menu. Default menu contains 2 items.
  
  
- create_order --username user --pizza_ids list_of_pizza_ids_separated_by_commas
  
  Creates a new order with the specified pizzas.
  Arguments:
  - --username <user_name>: The username of the customer placing the order.
  - --pizza_ids <list_of_pizza_ids>: A comma-separated list of pizza IDs to order.
    

- check_status --order_id order_id
  
  Checks the status of an existing order.
  Arguments:
  - --order_id <order_id>: The ID of the order to check.
    

- cancel_order --order_id order_id
  
  Cancels an existing order if it hasn't been marked as "ready to be delivered".
  Arguments:
  - --order_id <order_id>: The ID of the order to cancel.
    

### For admins
- add_pizza_admin --name new_pizza_name --price new_pizza_price
  
  Adds a new pizza to the menu.
  Arguments:
  - --name <new_pizza_name>: The name of the new pizza.
  - --price <new_pizza_price>: The price of the new pizza.
    
    
- cancel_order_admin --order_id order_id
  
  Cancels an order, regardless of its status.
  Arguments:
  - --order_id <order_id>: The ID of the order to cancel.
    

> [!NOTE]
> The actions `add_pizza_admin` and `cancel_order_admin` can only be executed by an admin and require the admin token (`--token supersecrettoken`) to be provided.

## Examples:
- `python3 client.py customer list_menu`
- `python3 client.py customer create_order --username John --pizza_ids 1,2,1`
- `python3 client.py customer check_status --order_id 55c2ceaf-7881-47fd-8543-5aff02ea44a1`
- `python3 client.py customer cancel_order --order_id 55c2ceaf-7881-47fd-8543-5aff02ea44a1`
- `python3 client.py admin add_pizza_admin --name Pineapple --price 30.02 --token supersecrettoken --token supersecrettoken`
- `python3 client.py admin cancel_order_admin --order_id 55c2ceaf-7881-47fd-8543-5aff02ea44a1`
