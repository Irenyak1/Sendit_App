from flask import Flask, request, jsonify, make_response
from api.models import User


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
