from flask import Flask, request, jsonify
from api.models import User, users_list, Order, orders_list
from api.validators import Validators


validators = Validators()


class User_Controller:

    def get_index_page(self):
        return jsonify({'status': 200,
                        'message': 'You are most welcome to our home page'})

    def signup_user(self):
        """This method allows the user to create an account
        """
        user_data = request.get_json()
        # get login data from user
        user_name = user_data.get('user_name')
        email = user_data.get('email')
        password = user_data.get('password')
        role = user_data.get('role')

        signup_validation = validators.validate_signup(user_data, user_name,
                                                       email, password, role)
        if signup_validation:
            return signup_validation

        for user in users_list:
            if user['user_name'] == user_name:
                return jsonify({'status': 400,
                               'message': 'This username is already taken '
                                'choose another username'})
        new_user = User(user_name, email, password, role)
        new_users = new_user.to_dict()

        users_list.append(new_user.to_dict())

        return jsonify({'status': 201,
                        'message': 'Thank you for signing up',
                        'new_user': new_users})

    def login(self):
        """ This method allows the user to login after cross checking their
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
                return jsonify({'status': 200,
                                'user': user,
                                'message': 'You have successfully logged in'})
        else:
            return jsonify({'status': 400,
                            'Error': 'Username or password did '
                            'not match any user'})

    def get_all_users(self):
        """
        Method to get all users that have
        signed up for accounts
        """

        if len(users_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no users yet'})
        else:
            return jsonify({'status': 200, 'users_list': users_list})

    def get_a_single_user(self, user_id):
        """Method to get a single user who has
           signed up for an account
        """
        if len(users_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no users yet'})
        for a_user in users_list:
            if a_user['user_id'] == user_id:
                return jsonify({'status': 200,
                                'user': a_user})
        return jsonify({'status': 400,
                        'message': 'There is no such user in the list.'})


class Order_Controller:

    def create_a_delivery_order(self):
        """ This method allows a user to create a delivery order.
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

    def get_all_orders(self):
        """
        Method for the admin to get all delivery orders
        created by users
        """

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no delivery orders yet'})

        else:
            return jsonify({'status': 200,
                            'orders_list': orders_list})

    def get_a_delivery_order(self, order_id):
        """ Method to fetch a single delivery order using order id """
        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no delivery orders yet'})

        for order in orders_list:
            if order['order_id'] == order_id:
                return jsonify({'status': 200,
                                'order': order})

        return jsonify({'status': 400,
                        'message': 'There is no such delivery '
                        'order in the list.'})

    # def get_all_delivery_orders_by_a_user(self, user_id):
    #     """ Method to fetch all delivery orders made by a user by user id """
    #     if len(orders_list) < 1:
    #         return jsonify({'status': 400,
    #                         'message': 'There are no orders placed yet'})

    #     for orders in orders_list:
    #         if orders['user_id'] == user_id:
    #             return jsonify({'status': 200,
    #                             'order': orders})

    #     return jsonify({'status': 400,
    #                     'message': 'The user has no orders yet.'})

    def get_a_delivery_order_by_a_user(self, order_id, user_id):
        """ Method to fetch a single delivery order by a user """

        if len(orders_list) < 1:
            return jsonify({'status': 400,
                            'message': 'There are no orders yet'})

        for order in orders_list:
            if order['user_id'] == user_id and order['order_id'] == order_id:
                return jsonify({'status': 200,
                                'order': order})

        return jsonify({'status': 400,
                        'message': 'Such order in not found in the list.'})

    def cancel_order(self, order_id):
        """Method to cancel a delivery order by order id"""

        order_data = request.get_json()
        status = order_data.get('status')

        cancel_order_validation = validators.validate_cancel_order(order_data,
                                                                   status)
        if cancel_order_validation:
            return cancel_order_validation

        for an_order in orders_list:
            if an_order['order_id'] == order_id:
                an_order["status"] = status
                return jsonify({'status': 200,
                                'order': an_order,
                                'message': 'Delivery order has '
                                'been cancelled'})

        return jsonify({'status': 400,
                        'message': 'The order has not been found'})

    def cancel_user_order(self, order_id, user_id):
        """Method to cancel a delivery order created by a particular user"""
        order_data = request.get_json()
        status = order_data.get('status')

        cancel_userorder_valid = validators.valid_cancel_user_order(order_data,
                                                                    status)
        if cancel_userorder_valid:
            return cancel_userorder_valid

        for order in orders_list:
            if order['order_id'] == order_id and order['user_id'] == user_id:
                order["status"] = status
                return jsonify({'status': 200,
                                'order': order,
                                'message': 'Delivery order by the user '
                                'has been cancelled'})

        return jsonify({'status': 400,
                        'message': 'Such order is not found '
                        'in the orders list'})

    # def cancel_userorders(self, user_id):
    #     """Method to cancel all delivery orders created by a user"""
    #     order_data = request.get_json()
    #     status = order_data.get('status')

    #     cancel_userorders_val = validators.valid_cancel_userorders(order_data,
    #                                                                status)

    #     if cancel_userorders_val:
    #         return cancel_userorders_val

    #     for order in orders_list:
    #         if order['user_id'] == user_id:
    #             order["status"] = status
    #             return jsonify({'status': 200,
    #                             'order': order,
    #                             'message': 'All delivery orders by the user '
    #                             'have been cancelled'})

    #     return jsonify({'status': 400,
    #                     'message': 'User has no orders yet'})
