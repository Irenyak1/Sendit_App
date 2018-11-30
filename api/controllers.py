from flask import Flask, request, jsonify
from api.models import User, USERS, Order, ORDERS
import re


class Controller_User:

    def get_index_page():
        return "You are most welcome to our home page"
        # return jsonify({'message': 'You are most welcome to our home page'}), 200

    def signup_user():
        """This method allows the user to create an account
        """
        user_data = request.get_json()
        # get login data from user
        user_name = user_data.get('user_name')
        email = user_data.get('email')
        password = user_data.get('password')
        role = user_data.get('role')
        user_id = len(USERS) + 1

        if not user_data:
            return jsonify({'message': 'Please fill all the feilds'}), 400

        if not user_name or user_name.isspace():
            return jsonify({'message': 'User name should be filled'}), 400

        if type(user_name) == int or len(user_name) < 5:
            return jsonify({
                'message': 'Username must be a string of at least 5 characters'
            }), 400

        if not email or email.isspace():
            return jsonify({'message': 'Please email is required'}), 400

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return jsonify({"message": "Please enter a valid email"}), 400

        if not password or password.isspace():
            return jsonify({'message': 'Password should be filled'}), 400

        if len(password) <= 5:
            return jsonify({
                'message': 'sorry! the password must be more than 5 characters'
            }), 400

        if not role or role.isspace():
            return jsonify({
                'message': 'sorry! the role should be filled as either admin or user'
            }), 400

        if type(role) == int or len(role) < 4 or len(role) > 5:
            return jsonify({
                'message': 'Role must be a string of 4 or 5 characters'
            }), 400

        for user in USERS:
            user_dict = user.to_dict()
            if user_dict['user_name'] == user_name:
                return jsonify({
                    'message': f"{user_name} already signed up choose another username"
                }), 400

        new_user = User(user_name, email, password, role, user_id)
        USERS.append(new_user)

        return jsonify({'message': f"Thank you {user_name} for signing up"}), 201

    def login(self):
        """ This method allows the user to login after cross checking their
            user_name, password, user role and user id.
        """
        user_data = request.get_json()
        # get login data from user
        user_name = str(user_data.get('user_name')).strip()
        password = user_data.get('password')
        role = str(user_data.get('role')).strip()
        user_id = len(USERS) + 1

        if not user_data:
            return jsonify({'message': 'All fields are required'}), 400

        if not user_name or user_name == " ":
            return jsonify({'message': 'username is required'}), 400

        if not password or password == " ":
            return jsonify({'message': 'Fill in the password'}), 400

        if not role or role == " ":
            return jsonify({'message': 'Fill in your role'}), 400

        return jsonify({"message": f"Welcome {role}, You are logged in"}), 201

    def get_all_users(self):
        """
        Method for the admin to get all users that have signed up 
        for accounts
        """
        if User.role == 'admin':
            return jsonify(USERS), 200
        return jsonify({'message': 'You have no rights to access users'}), 400


class Controller_Order:

    def create_a_delivery_order(self):
        """ This method allows a user to create a delivery order.
            And it also generates the order_id automatically.
        """
        if User.role == 'user':
            order_data = request.get_json()
            # get sale data
            user_id = order_data.get('user_id')
            user_name = order_data.get('user_name')
            contact = order_data.get('contact')
            pickup_location = order_data.get('pickup_location')
            destination = order_data.get('destination')
            weight = order_data.get('weight')
            price = order_data.get('price')
            order_id = len(ORDERS) + 1

            if not order_data or order_data.isspace():
                return jsonify({'message': 'Please fill all the feilds'}), 400

            if not user_id or user_id == "":
                return jsonify({
                    'message': 'Oops! fill in user_id and should be an integer'
                }), 400

            if type(user_id) != int or user_id == 0:
                return jsonify({
                    'message': 'sorry! the user_id must be an integer > 0'
                }), 400

            if not user_name or user_name == "":
                return jsonify({
                    'message': 'User name can not be an empty string.'
                }), 400

            if type(user_name) == int or len(user_name) <= 5:
                return jsonify({
                    'message': 'Username must be more than 5 letters'
                }), 400

            if not contact or contact == "":
                return jsonify({
                    'message': 'Contact is required, it should not be blank.'
                }), 400

            if type(contact) != int or len(contact) < 10 or len(contact) > 12:
                return jsonify({
                    'message': 'Contact should contain 10 to 12 figures'
                }), 400

            if not pickup_location or pickup_location.isspace():
                return jsonify({
                    'message': 'Pickup location can not be an empty string.'
                }), 400

            if not destination or destination.isspace():
                return jsonify({
                    'message': 'Please! the destination can no be empty.'
                }), 400

            if type(destination) == int or len(destination) <= 4:
                return jsonify({
                    'message': 'Destination must have atleast 4 letters.'
                }), 400

            if not weight or weight == "":
                return jsonify({
                    'message': 'Destination can not be an empty string.'
                }), 400

            if type(weight) != int:
                return jsonify({
                    'message': 'Sorry! the weight should be an integer.'
                }), 400

            if not price or price == "":
                return jsonify({
                    'message': 'Please! the price is required '
                }), 400

            if type(price) != int:
                return jsonify({
                    'message': 'Please! the price is required as an integer.'
                }), 400

            for order in ORDERS:
                order_dict = order.to_dict()
                if order_dict['order_id'] == order_id:
                    return jsonify({
                        'message': "Delivery order already exists."
                    }), 400

            new_order = Order(user_id, user_name, contact,
                              pickup_location, destination,
                              weight, price, order_id)
            ORDERS.append(new_order)

            if new_order:
                return jsonify({
                    'message': 'Delivery order created!',
                    'new_order': new_order
                }), 201

        return jsonify({
            'message': 'Only users are allowed to create orders.'
        }), 400

    def get_all_orders(self):
        """
        Method for the admin to get all delivery orders
        created by users
        """
        if User.role == 'admin':
            return jsonify(ORDERS), 200
        return jsonify({
            'message': 'You have no rights to view all orders'
        }), 400

    def get_a_delivery_order(self, order_id):
        """ Method to fetch a single delivery order using order id """
        for order_list in ORDERS:
            if order_list['order_id'] == order_id:
                return jsonify(order_list), 200
        return jsonify({
            'message': 'There is no such delivery order in the list.'
        }), 400

    def get_delivery_order(self, user_id):
        """ Method to fetch a single delivery order using user id """
        for order_list in ORDERS:
            if order_list['user_id'] == user_id:
                return jsonify(order_list), 200
        return jsonify({
            'message': 'That order is not found in the list.'
        }), 400

    def cancel_order(self, order_id):
        """Method to cancel a delivery order by order id"""
        for order in ORDERS:
            order_dict = order.to_dict()
            if order_dict['order_id'] == order_id:
                order_dict["status"] = "cancelled"
                return jsonify({
                    "Delivery_order_has_been_cancelled": order_dict}), 200
        return jsonify({'message': 'The order has not been found'}), 200

    def cancel_an_order_by_a_user(self, order_id, user_id):
        """Method to cancel a delivery order created by a particular user"""
        for order in ORDERS:
            order_dict = order.to_dict()
            if order_dict['order_id'] == order_id and order_dict['user_id'] == user_id: 
                order_dict["status"] = "cancelled"
                return jsonify({"The order is cancelled":order_dict}), 200
            return jsonify({'message':'You dont have rights to cancel this delivery order'}), 200
        return jsonify({'message':'The search did not match any order'}), 200