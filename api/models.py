from flask import Flask, request, jsonify, make_response


def get_index_page():
    return "You are most welcome to our home page"

""" This is a global variable called USERS """
USERS = [{"username": "admin", "password": "admin", "role": "admin"},
         {"username": "Maxie", "password": "elite", "role": "user"}]


class User:
    """
    This class defines the user in terms of
    the username, password and user_role.
    """

    user_role = ""

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def login(self):
        """ This method allows the user to login after cross checking their
            username, password and user role
        """
        for user in USERS:
            if user['username'] == self.username and user['password'] == self.password and user['role'] == self.role:
                User.user_role = self.role
        return self.user_role


class Order:
    """
    This class defines a parcel delivery order in terms of
    user_id, user_name, contact, order_id, pickup_location, destination, weight, price.
    """

    ORDERS = []
    """
    This is a list that will store all the deliverry orders
    that will be  created.
    """

    def __init__(self, user_id, user_name, contact,
                 pickup_location, destination, weight, price):
        self.user_id = user_id
        self.user_name = user_name
        self.contact = contact
        self.pickup_location = pickup_location
        self.destination = destination
        self.weight = weight
        self.price = price
    
    def create_a_delivery_order(self):
        """ This method allows a user to create a delivery order.
            And it also generates the order_id automatically.
        """
        if User.user_role == 'user':
            my_orders = dict
            if not Order.ORDERS:
                order_id = 1
        else:
            order_id = Order.ORDERS[-1].get('order_id') + 1

        self.my_orders = {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'contact': self.contact,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'weight': self.weight,
            'price': self.price,
            'order_id': order_id
        }

        Order.ORDERS.append(self.my_orders)

        return 'You have created a delivery order.'


        