import re
from flask import jsonify


class Validators:

    def validate_signup(self, user_data, user_name, email, password, role):

        if not user_data or user_data == "":
            return jsonify({'status': 400,
                            'message': 'Please fill all the feilds'})

        if not isinstance(user_name, str):
            return jsonify({'status': 400,
                            'message': 'User name must be a string'})

        if not user_name.isalpha():
            return jsonify({'status': 400,
                            'message': 'User name should be '
                            'alphabetical letters'})

        if not user_name or user_name.strip() == "":
            return jsonify({'status': 400,
                            'message': 'User name should be filled'})

        if not user_name or len(user_name) < 5:
            return jsonify({'status': 400,
                            'message': 'Username must be a string of at '
                                       'least 5 characters'})

        if not email or email == "":
            return jsonify({'status': 400,
                            'message': 'Please email is required'})

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return jsonify({'status': 400,
                            'message': 'Please enter a valid email'}), 400

        if not password or password.strip() == "":
            return jsonify({'status': 400,
                            'message': 'Password should be filled'})

        if not password or len(password) < 6:
            return jsonify({'status': 400,
                            'message': 'sorry! password must be at least '
                            '6 characters'})

        if not role or role == "":
            return jsonify({'status': 400,
                            'message': 'sorry! the role should be filled as '
                            'either admin or user'})
        if not isinstance(role, str):
            return jsonify({'status': 400,
                            'message': 'Role must be a string'})

        if not role or len(role) < 4 or len(role) > 5:
            return jsonify({'status': 400,
                            'message': 'Role must be a string of 4 or '
                            '5 characters'})

        if not role.isalpha():
            return jsonify({'status': 400,
                            'message': 'Role should be '
                            'alphabetical letters'})

        # if not role or role != user or role != admin:
        #     return jsonify({'status': 400,
        #                     'message': 'Role must be either user or admin'})

    def validate_login(self, user_data, user_name, password):

        if not user_data or user_data == "":
            return jsonify({'status': 400,
                            'message': 'All fields are required'})

        if not user_name or user_name == "":
            return jsonify({'status': 400,
                            'message': 'Username can not be empty'})

        # if not user_name or user_name.strip() == "":
        #     return jsonify({'status': 400,
        #                     'message': 'User name should be filled'})

        if not isinstance(user_name, str):
            return jsonify({'status': 400,
                            'message': 'User name should be a string'})

        if not user_name.isalpha():
            return jsonify({'status': 400,
                            'message': 'User name should be '
                            'alphabetical letters'})

        if not user_name or len(user_name) < 5:
            return jsonify({'status': 400,
                            'message': 'Username must be a string of '
                            'at least 5 characters'})

        if not password or password == " ":
            return jsonify({'status': 400,
                            'message': 'Fill in the password'})

        if not password or len(password) < 5:
            return jsonify({'status': 400,
                            'message': 'Password must be of '
                            'at least 5 characters'})

    def validate_create_order(self, order_data, user_id, user_name, contact,
                              pickup_location, destination, weight,
                              price, status):
        if not order_data or order_data == "":
            return jsonify({'status': 400,
                            'message': 'Please fill in order data'})

        if not user_id or user_id == "":
            return jsonify({'status': 400,
                            'message': 'Oops! fill in user_id '
                            'and should be an integer'})

        if not isinstance(user_id, int):
            return jsonify({'status': 400,
                            'message': 'sorry! the user id '
                            'must be an integer'})
        
        if not user_id or user_id < 1:
            return jsonify({'status': 400,
                            'message': 'sorry! the user id '
                            'can not be less than 1'})

        if not user_name or user_name == "":
            return jsonify({'status': 400,
                            'message': 'Username can not be '
                            'an empty string'})

        # if not user_name or user_name.strip() == "":
        #     return jsonify({'status': 400,
        #                     'message': 'User name should be filled'})

        if not isinstance(user_name, str):
            return jsonify({'status': 400,
                            'message': 'User name must be a string'})

        if not user_name.isalpha():
            return jsonify({'status': 400,
                            'message': 'User name must be '
                            'alphabetical letters'})

        if not user_name or len(user_name) < 5:
            return jsonify({'status': 400,
                            'message': 'Username should be a string of '
                                       'at least 5 characters'})

        if not contact or contact == "":
            return jsonify({'status': 400,
                            'message': 'Contact is required '
                            'it should not be blank'})

        if not isinstance(contact, int):
            return jsonify({'status': 400,
                            'message': 'Contact should be an interger '
                                       'of 7 to 15 digits'})

        # if not contact or len(contact) < 7 or len(contact) > 15:
        #     return jsonify({'status': 400,
        #                     'message': 'Contact length should be '
        #                     '7 to 15 digits.'})

        if not pickup_location or pickup_location == "":
            return jsonify({'status': 400,
                            'message': 'Pickup location can not be '
                            'an empty string'})

        if not isinstance(pickup_location, str):
            return jsonify({'status': 400,
                            'message': 'Pickup location must be '
                            'a string'})

        if not pickup_location.isalpha():
            return jsonify({'status': 400,
                            'message': 'Pickup location must be '
                            'alphabetical letters'})

        if not pickup_location or len(pickup_location) < 4:
            return jsonify({'status': 400,
                            'message': 'Pickup location must have '
                            'at least 4 letters'})

        if not destination or destination == "":
            return jsonify({'status': 400,
                            'message': 'Please! the destination '
                            'can not be empty'})

        if not isinstance(destination, str):
            return jsonify({'status': 400,
                            'message': 'Fill destination as a string'})

        if not destination.isalpha():
            return jsonify({'status': 400,
                            'message': 'Fill destination as alphabetical '
                                       'letters'})

        if not destination or len(destination) < 4:
            return jsonify({'status': 400,
                            'message': 'Destination must have '
                            'atleast 4 letters'})

        if not weight or weight == "":
            return jsonify({'status': 400,
                            'message': 'Please the weight is required'})

        if not isinstance(weight, int):
            return jsonify({'status': 400,
                            'message': 'sorry! the weight '
                            'must be an integer > 0'})

        if not weight or weight < 1:
            return jsonify({'status': 400,
                            'message': 'sorry! the weight '
                            'must be greater than 0'})
        if not price or price == "":
            return jsonify({'status': 400,
                            'message': 'Please the price should be filled'})

        if not isinstance(price, int):
            return jsonify({'status': 400,
                            'message': 'Please! the price is '
                            'required as an integer'})

        if not price or price < 1:
            return jsonify({'status': 400,
                            'message': 'The price can not be less than 1'})

        if not status or status == "":
            return jsonify({'status': 400,
                            'message': 'Fill in the status as either pending, '
                            'delivered or canceled'})

        if not isinstance(status, str):
            return jsonify({'status': 400,
                            'message': 'The status should be a string'})

        if not status.isalpha():
            return jsonify({'status': 400,
                            'message': 'Status should be '
                            'alphabetical letters'})

        if not status or len(status) < 4:
            return jsonify({'status': 400,
                            'message': 'Fill the status as a string, '
                            'of at least 4 letters'})

    def validate_cancel_order(self, order_data, status):
        if not order_data or order_data == "":
            return jsonify({'status': 400,
                            'message': 'Please fill all the '
                            'required feilds'})

        if not status or status == " ":
            return jsonify({'status': 400,
                            'message': 'Please fill in the status '
                            'of the order'})

    def validate_cancel_orders(self, order_data, status):
        if not order_data or order_data == "":
            return jsonify({'status': 400,
                            'message': 'Fill in all the '
                            'required feilds'})

        if not status or status == " ":
            return jsonify({'status': 400,
                            'message': 'Please provide the status '
                            'of the order'})

    def valid_cancel_user_order(self, order_data, status):
        if not order_data or order_data == "":
            return jsonify({'status': 400,
                            'message': 'Please fill all the feilds required'})
        if not status or status == " ":
            return jsonify({'status': 400,
                            'message': 'Please fill in the status '
                            'of the order'})

    def valid_cancel_userorders(self, order_data, status):
        if not order_data or order_data == "":
            return jsonify({'status': 400,
                            'message': 'Please fill the required feilds'})
        if not status:
            return jsonify({'status': 400,
                            'message': 'Please fill in the status '
                            'of the order'})
