from flask import Flask, request, jsonify
from api.models import User, users_list, Order, orders_list
from api.validators import Validators
import jwt
import datetime
from functools import wraps


validators = Validators()


class User_Controller:

    @staticmethod
    def get_index_page():
        return jsonify({'status': 200,
                        'message': 'You are most welcome to our home page'})

    @staticmethod
    def signup_user():
        """
        This method allows the user to create an account
        """
        user_data = request.get_json()
        user_name = user_data.get('user_name')
        email = user_data.get('email')
        password = user_data.get('password')
        role = user_data.get('role')

        signup_validation = validators.validate_signup(user_data, user_name,
                                                       email, password, role)
        if signup_validation:
            return signup_validation

        for user in users_list:
            if user['user_name'] == user_name or user['email'] == email:
                return jsonify({'status': 400,
                                'message': 'This username or email already '
                                'taken choose another username or email'})

        new_user = User(user_name, email, password, role)
        new_users = new_user.to_dict()

        users_list.append(new_user.to_dict())

        return jsonify({'status': 201,
                        'message': 'Thank you for signing up',
                        'new_user': new_users})

    @staticmethod
    def login():
        """
        This method allows the user to login after cross checking their
        user_name, password, user role and user id.

        """
        user_data = request.get_json()
        user_name = user_data.get('user_name')
        password = user_data.get('password')

        login_validation = validators.validate_login(user_data, user_name,
                                                     password)
        if login_validation:
            return login_validation

        for user in users_list:
            if user['user_name'] == user_name and user['password'] == password:
                if user['user_name'] == 'admin' and user['password'] == 'admin123':
                    admins_token = jwt.encode({'user_name': user_data['user_name'],
                                               'exp': datetime.datetime.utcnow() +
                                               datetime.timedelta(minutes=30)}, 'access')
                    return jsonify({'status': 200,
                                    'message': 'Welcome admin',
                                    'user': user,
                                    'token': admins_token.decode('utf-8')})

                if user['user_name'] != 'admin' and user['password'] != 'admin123':
                    users_token = jwt.encode({'user_name': user_data['user_name'],
                                              'exp': datetime.datetime.utcnow() +
                                              datetime.timedelta(minutes=30)}, 'nogo')
                    return jsonify({'status': 200,
                                    'message': 'You have successfully '
                                               'logged in',
                                    'user': user,
                                    'token': users_token.decode('utf-8')})
        else:
            return jsonify({'status': 400,
                            'message': 'Username or password did '
                            'not match any user'})

    @staticmethod
    def get_all_users():
        """
        Method to get all users that have
        signed up for accounts
        """

        if len(users_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no users yet'})
        else:
            return jsonify({'status': 200, 'users_list': users_list})

    @staticmethod
    def get_a_single_user(user_id):
        """
        Method to get a single user who has
        signed up for an account
        """
        if len(users_list) < 1:
            return jsonify({'status': 400,
                            'message': 'No users to display'})
        for a_user in users_list:
            if a_user['user_id'] == user_id:
                return jsonify({'status': 200,
                                'user': a_user})
        return jsonify({'status': 400,
                        'message': 'There is no such user in the list'})


class Order_Controller:

    @staticmethod
    def create_a_delivery_order():
        """
        This method allows a user to create a delivery order.
        And it also generates the order_id automatically.
        """

        order_data = request.get_json()
        user_id = order_data.get('user_id')
        user_name = order_data.get('user_name')
        contact = order_data.get('contact')
        pickup_location = order_data.get('pickup_location')
        destination = order_data.get('destination')
        weight = order_data.get('weight')
        price = order_data.get('price')
        status = order_data.get('status')

        order_validation = validators.validate_create_order(order_data,
                                                            user_id,
                                                            user_name,
                                                            contact,
                                                            pickup_location,
                                                            destination,
                                                            weight,
                                                            price,
                                                            status)
        if order_validation:
            return order_validation

        order = Order(user_id, user_name, contact, pickup_location,
                      destination, weight, price, status)
        new_order = order.to_dict()
        orders_list.append(order.to_dict())

        return jsonify({'status': 201,
                        'message': 'Delivery order created!',
                        'new_order': new_order})

    @staticmethod
    def get_all_orders():
        """
        Method to get all delivery orders
        created by user
        """

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no delivery orders yet'})

        else:
            return jsonify({'status': 200,
                            'orders_list': orders_list})

    @staticmethod
    def get_a_delivery_order(order_id):
        """ Method to fetch a single delivery order using order id """

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'You have no orders yet'})

        for order in orders_list:
            if order['order_id'] == order_id:
                return jsonify({'status': 200,
                                'order': order})

        return jsonify({'status': 400,
                        'message': 'There is no such delivery '
                        'order in the list'})

    @staticmethod
    def get_all_delivery_orders_by_a_user(user_id):
        """ Method to fetch all delivery orders made by a specific user """
        my_orders = []

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no orders placed yet'})

        for order in orders_list:
            if order['user_id'] == user_id:
                my_orders.append(order)
        if my_orders:
            return jsonify({'status': 200,
                            'number of orders placed': len(my_orders),
                            'my_orders': my_orders})

        return jsonify({'status': 400,
                        'message': 'The user has no orders yet or the '
                        'user does not exist'})

    @staticmethod
    def get_a_delivery_order_by_a_user(order_id, user_id):
        """ Method to fetch a single delivery order by a user """

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no orders yet'})

        for order in orders_list:
            if order['user_id'] == user_id and order['order_id'] == order_id:
                return jsonify({'status': 200,
                                'order': order})

        return jsonify({'status': 400,
                        'message': 'The user has no such order '
                        'or the user does not exist in the list'})

    @staticmethod
    def cancel_order(order_id):
        """Method to cancel a delivery order by order id"""

        order_data = request.get_json()
        status = order_data.get('status')

        cancel_order_validation = validators.validate_object(order_data,
                                                             status)
        if cancel_order_validation:
            return cancel_order_validation

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no orders in the list yet'})

        for an_order in orders_list:
            if an_order['order_id'] == order_id:
                if an_order["status"] == "pending":
                    an_order["status"] = status
                    return jsonify({'status': 200,
                                    'order': an_order,
                                    'message': 'Delivery order has '
                                    'been cancelled'})

        return jsonify({'status': 400,
                        'message': 'The order has not been found'})

    @staticmethod
    def cancel_user_order(order_id, user_id):
        """Method to cancel a delivery order created by a particular user"""
        order_data = request.get_json()
        status = order_data.get('status')

        cancel_userorder_valid = validators.validate_object(order_data,
                                                            status)
        if cancel_userorder_valid:
            return cancel_userorder_valid

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'No delivery orders to cancel'})

        for order in orders_list:
            if order['order_id'] == order_id and order['user_id'] == user_id:
                if order["status"] == "pending":
                    order["status"] = status
                    return jsonify({'status': 200,
                                    'order': order,
                                    'message': 'Pending order by the user '
                                    'has been cancelled'})

        return jsonify({'status': 400,
                        'message': 'The order is not found '
                        'in the orders list or the user does not exist'})

    @staticmethod
    def cancel_userorders(user_id):
        """Method to cancel all delivery orders created by a user"""
        my_cancelled_orders = []

        order_data = request.get_json()
        status = order_data.get('status')

        cancel_userorders_val = validators.validate_object(order_data,
                                                           status)

        if cancel_userorders_val:
            return cancel_userorders_val

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'No orders to cancel'})

        for order in orders_list:
            if order['user_id'] == user_id and order["status"] == "pending":
                order["status"] = status
                my_cancelled_orders.append(order)
        if my_cancelled_orders:
                return jsonify({'status': 200,
                                'number of cancelled '
                                'orders': len(my_cancelled_orders),
                                'my_cancelled_orders': my_cancelled_orders,
                                'message': 'All pending orders by the user '
                                'have been cancelled'})

        return jsonify({'status': 400,
                        'message': 'User has no orders to cancel or user '
                        'does not exist'})

    @staticmethod
    def cancel_orders():
        """Method to cancel all delivery orders"""
        all_cancelled_orders = []

        order_data = request.get_json()
        status = order_data.get('status')

        cancel_orders_valid = validators.validate_object(order_data,
                                                         status)
        if cancel_orders_valid:
            return cancel_orders_valid

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no delivery '
                            'orders to cancel'})

        for any_order in orders_list:
            if any_order["status"] == "pending":
                any_order["status"] = status
                all_cancelled_orders.append(any_order)
        if all_cancelled_orders:
                return jsonify({'status': 200,
                                'Orders cancelled': len(all_cancelled_orders),
                                'all_cancelled_orders': all_cancelled_orders,
                                'message': 'All pending orders have '
                                'been cancelled'})

        return jsonify({'status': 400,
                        'message': 'The orders can not be cancelled'})
