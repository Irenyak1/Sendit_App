from flask import Flask, jsonify
from api.models import User, Order
from api.controllers import User_Controller, Order_Controller


app = Flask(__name__)

usercontroller = User_Controller()
ordercontroller = Order_Controller()

@app.route('/', methods=['GET'])
def index():
    """ Endpoint to get the index page of the application"""
    return usercontroller.get_index_page()


@app.route('/api/v1/signup', methods=['POST'])
def signup_user():
    """ Endpoint to signup a user """
    return usercontroller.signup_user()


@app.route('/api/v1/login', methods=['POST'])
def login():
    """ Endpoint for a user to login """
    return usercontroller.login()


@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    """ Endpoint for the admin to get all users that have signed up 
        for accounts """
    return usercontroller.get_all_users()
    

@app.route('/api/v1/orders', methods=['POST'])
def create_a_delivery_order():
    """ Endpoint to create a delivery order by the user """
    return ordercontroller.create_a_delivery_order()

@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    """ Endpoint for the admin to get all delivery orders
        created by users
    """
    return ordercontroller.get_all_orders()

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_a_delivery_order(order_id):
    """ Endpoint to fetch a single delivery order using order id """
    return ordercontroller.get_a_delivery_order(order_id)


@app.route('/api/v1/orders/users/<int:user_id>', methods=['GET'])
def get_delivery_order(user_id):
    """ Endpoint to fetch a single delivery order using user id  """
    return ordercontroller.get_delivery_order(user_id)


@app.route('/api/v1/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    """ Endpoint to cancel a single delivery order by user id  """
    return ordercontroller.cancel_order(order_id)

@app.route('/api/v1/users/<int:user_id>/<int:order_id>/cancel', methods = ['PUT'])
def cancel_an_order_by_a_user(order_id, user_id):
    """Cancel a delivery order by a user"""
    return ordercontroller.cancel_an_order_by_a_user(order_id, user_id)
