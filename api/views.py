from flask import Flask, request, jsonify, make_response
from api.models import User, Order


app = Flask(__name__)


@app.route('/')
def index():
    """ Endpoint to get the index page of the application"""
    my_response = "You are most welcome to our home page"
    return jsonify(my_response), 200


@app.route('/auth/login', methods=['POST'])
def login():
    """ Endpoint for a user to login """
    user_data = request.get_json()
    # get login data from user
    name = user_data.get('username')
    password = user_data.get('password')
    role = user_data.get('role')

    user = User(name, password, role)
    login_result = user.login()

    if login_result:
        return jsonify('Welcome {}'.format(login_result)), 200
    return jsonify({
                'message': 'Sorry please login with the right credentials'
                }), 400

@app.route('/api/v1/orders', methods=['POST'])
def create_a_delivery_order():
    """ Endpoint to create a delivery order by the user """
    if User.user_role == 'user':
        order_data = request.get_json()
        # get sale data
        user_id = order_data.get('user_id')
        user_name = order_data.get('user_name')
        contact = order_data.get('contact')
        pickup_location = order_data.get('pickup_location')
        destination = order_data.get('destination')
        weight = order_data.get('weight')
        price = order_data.get('price')
     
        # validate sale data
        if not order_data:
            return jsonify({'message': 'Please fill all the feilds'}), 400

        if not user_id or user_id == "":
            return jsonify({
                'message': 'Oops! fill in user_id and should be an integer'
            }), 400

        if not user_name or user_name == "":
            return jsonify({
                'message': 'sorry! user name is required and can not be an empty string.'
            }), 400

        if not contact or contact == "":
            return jsonify({
                'message': 'Please! the contact is required, it should not be blank.'
            }), 400
       
        if type(contact) != int:
            return jsonify({
                'message': 'Please the contact should be an integer.'
            }), 400

        if not pickup_location  or pickup_location == "":
            return jsonify({
                'message': 'Please! pickup location is required and can not be an empty string.'
            }), 400
        
        if not destination  or destination == "":
            return jsonify({
                'message': 'Please! the destination is required and can not be an empty string.'
            }), 400
        
        if not weight  or weight == "":
            return jsonify({
                'message': 'Please! the destination is required and can not be an empty string.'
            }), 400

        if type(weight) != int:
            return jsonify({
                'message': 'Please! the weight should be filled as an integer.'
            }), 400
        
        if not price or price == "":
            return jsonify({
                'message': 'Please! the price is required '
            }), 400

        if type(weight) != int:
            return jsonify({
                'message': 'Please! the price is required as an integer.'
            }), 400

        new_order = Order(user_id, user_name, contact, pickup_location, destination, weight, price)
        result_create_a_delivery_order = new_order.create_a_delivery_order()

        if result_create_a_delivery_order:
            return jsonify({'message': 'Sale order created successfully',
                            'new_order': new_order
                          }), 201

    return jsonify({'message': 'You can not create a delivery order if you are not a user.'}), 400
