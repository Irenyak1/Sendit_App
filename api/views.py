from flask import Flask, jsonify
from api.models import User, Order
from api.controllers import Controller_User, Controller_Order


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """ Endpoint to get the index page of the application"""
    # my_response = "You are most welcome to our home page"
    return Controller_User.get_index_page()


@app.route('/api/v1/signup', methods=['POST'])
def signup_user():
    """ Endpoint to signup a user """
    return Controller_User.signup_user()


@app.route('/api/v1/login', methods=['POST'])
def login():
    """ Endpoint for a user to login """
    return Controller_User.login()


@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """ Endpoint for the admin to get all users that have signed up 
        for accounts """
    if User.role == 'admin':
        return Controller_User.get_all_users()
    return jsonify({
            'message': 'You have no rights to access users'
            }), 400


@app.route('/api/v1/orders', methods=['POST'])
def create_a_delivery_order():
    """ Endpoint to create a delivery order by the user """
    if User.role == 'user':
        return Controller_Order.create_a_delivery_order()

    return jsonify({
            'message': 'Only users can create delivery orders.'
            }), 400


@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    """ Endpoint for the admin to get all delivery orders
        created by users
    """
    if User.role == 'admin':
        return Controller_Order.get_all_orders()

    return jsonify({'message': 'You have no rights to access orders'}), 400


@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_a_delivery_order(order_id):
    """ Endpoint to fetch a single delivery order using order id """
    return Controller_Order.get_a_delivery_order(order_id)


@app.route('/api/v1/orders/users/<int:user_id>', methods=['GET'])
def get_delivery_order(user_id):
    """ Endpoint to fetch a single delivery order using user id  """
    return Controller_Order.get_delivery_order(user_id)


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def cancel_order(order_id):
    """ Endpoint to cancel a single delivery order by user id  """
    return Controller_Order.cancel_order(order_id)

@app.route('/api/v1/users/<int:user_id>/<int:order_id>/cancel', methods = ['PUT'])
def cancel_an_order_by_a_user(order_id, user_id):
    """Cancel a delivery order by a user"""
    return Controller_Order.cancel_an_order_by_a_user(order_id, user_id)
