from flask import Flask, request, jsonify
from api.models import User, users_list, Order, orders_list
from api.validators import Validators


validators = Validators()

class User_Controller:

    def get_index_page(self):
        return jsonify({'status':200, 'message': 'You are most welcome to our home page'})

    def signup_user(self):
        """This method allows the user to create an account
        """
        user_data = request.get_json()
        # get login data from user
        user_name = user_data.get('user_name')
        email = user_data.get('email')
        password = user_data.get('password')
        role = user_data.get('role')

        signup_validation = validators.validate_signup(user_data, user_name, email, password, role )
        if signup_validation:
            return signup_validation

        for user in users_list:
            if user['user_name'] == user_name:
                return jsonify({
                    'message': 'This username is already signed up choose another username'
                }), 400

        new_user = User(user_name, email, password, role)
        new_users = new_user.to_dict()

        users_list.append(new_user.to_dict())

        
        return jsonify({ 'status': 201,
            'message': 'Thank you for signing up',
            'new_user': new_users
        })
        
    
    def login(self):
        """ This method allows the user to login after cross checking their
            user_name, password, user role and user id.
        """
        user_data = request.get_json()
        user_name = user_data.get('user_name')
        password = user_data.get('password')
        
        # if not user_data:
        #     return jsonify({'message': 'All fields are required'}), 400

        # if not user_name or user_name == " ":
        #     return jsonify({'message': 'username is required'}), 400

        # if not password or password == " ":
        #     return jsonify({'message': 'Fill in the password'}), 400

        # # if not role or role == " ":
        # #     return jsonify({'message': 'Fill in your role'}), 400

        
        # return jsonify({'message': 'Welcome, You are logged in'}), 201
       
        for user in users_list:
            if user['user_name'] == user_name and user['password'] == password:
                return jsonify({'status': 200,
                'user': user,
                'message':'You have successfully logged in'})
        else:
            return jsonify({'status': 400,
            'Error': 'Email or password did not match any user'})
            
    def get_all_users(self):
        """
        Method for the admin to get all users that have signed up 
        for accounts
        """
        if len(users_list) < 1:
            return jsonify({'status': 400,
                    'message': 'There are no users yet'}) 
        else:
            return jsonify({'status': 200, 'users_list' : users_list})


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
        

        if not order_data:
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

        if type(contact) != int:
            return jsonify({
                'message': 'Contact should be an interger of 8 to 12 figures'
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

        if not weight:
            return jsonify({
                'message': 'Destination can not be an empty string.'
            }), 400

        if type(weight) != int:
            return jsonify({
                'message': 'Sorry! the weight should be an integer.'
            }), 400

        if not price:
            return jsonify({
                'message': 'Please! the price is required '
            }), 400

        if type(price) != int:
            return jsonify({
                'message': 'Please! the price is required as an integer.'
            }), 400
        
        if not status or status== "":
            return jsonify({
                'message': 'Status can be either pending, delivered or cancelled.'
            }), 400

        order = Order(user_id, user_name, contact,pickup_location, destination,weight, price, status)
        new_order = order.to_dict()
        orders_list.append(order.to_dict())

       
        return jsonify({'status': 201,
                'message': 'Delivery order created!',
                'new_order': new_order
            })

    def get_all_orders(self):
        """
        Method for the admin to get all delivery orders
        created by users
        """
        
        if len(orders_list) < 1:
            return jsonify({'status':400,
                'message': 'There are no delivery orders yet'})
        
        else:
            return jsonify({'status':400,
            'orders_list': orders_list})
            

    def get_a_delivery_order(self, order_id):
        """ Method to fetch a single delivery order using order id """
        if len(orders_list) < 1:
            return jsonify({'status':400,
            'message': 'There are no delivery orders yet'})

        for order in orders_list:
            if order['order_id'] == order_id:
                return jsonify({'status':200, 
                'order': order})
        
        return jsonify({'status': 400, 
            'message': 'There is no such delivery order in the list.'})

    def get_delivery_order(self, user_id):
        """ Method to fetch a single delivery order using user id """
        
        if len(orders_list) < 1:
            return jsonify({'status':400,
            'message': 'There are no orders placed yet'})

        for one_order in orders_list:
            if one_order['user_id'] == user_id:
                return jsonify({'status':200, 
                'order': one_order})
        
        return jsonify({'status': 400, 
            'message': 'That order is not found in the list.'})


    def cancel_order(self, order_id):
        """Method to cancel a delivery order by order id"""
        
        order_data = request.get_json()
        status = order_data.get('status')
        
        if not order_data:
            return jsonify({'message': 'Please fill all the feilds'}), 400
        if not status:
            return jsonify({'message': 'Please fill in the status of the order'}), 400

        for an_order in orders_list:
            if an_order['order_id'] == order_id:
                an_order["status"] = status
                return jsonify({'status': 200,
                        'message': 'Delivery order has been cancelled'})

        return jsonify({'status': 400, 'message': 'The order has not been found'}), 200

    def cancel_an_order_by_a_user(self, order_id, user_id):
        """Method to cancel a delivery order created by a particular user"""
        order_data = request.get_json()
        status = order_data.get('status')

        if not order_data:
            return jsonify({'message': 'Please fill all the feilds'}), 400
        if not status:
            return jsonify({'message': 'Please fill in the status of the order'}), 400

        for anorder in orders_list:
            if anorder['order_id'] == order_id and anorder['user_id'] == user_id:
                anorder["status"] = status
                return jsonify({'status': 200,
                        'message': 'Delivery order by a certain user has been cancelled'})
        
        return jsonify({'status': 400, 'message': 'Such order is not found in the orders list'})

        