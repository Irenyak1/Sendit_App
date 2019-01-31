import re
from flask import jsonify


class Validators:

    def validate_signup(self, user_data, user_name, email, password, role):

        if not user_data:
            return jsonify({'status': 400,
                            'message': 'Please fill all the feilds'})

        if not isinstance(user_name, str):
            return jsonify({'status': 400,
                            'message': 'User name should be a string'})

        if not user_name.isalpha():
            return jsonify({'status': 400,
                            'message': 'User name should be '
                            'alphabetical letters'})

        if not user_name or user_name.strip() == "":
            return jsonify({'status': 400,
                            'message': 'User name should be filled'})

        if type(user_name) == int or len(user_name) < 5:
            return jsonify({'status': 400,
                            'message': 'Username must be a string of '
                            'at least 5 characters'})

        if not email or email == "":
            return jsonify({'status': 400,
                            'message': 'Please email is required'})

        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return jsonify({'status': 400,
                            'message': 'Please enter a valid email'}), 400

        if not password or password.strip() == "":
            return jsonify({'status': 400,
                            'message': 'Password should be filled'})

        if not password or len(password) <= 5:
            return jsonify({'status': 400,
                            'message': 'sorry! the password must be more than '
                            '5 characters'})

        if not role or role.strip() == "":
            return jsonify({'status': 400,
                            'message': 'sorry! the role should be filled as '
                            'either admin or user'})

        if type(role) == int or len(role) < 4 or len(role) > 5:
            return jsonify({'status': 400,
                            'message': 'Role must be a string of 4 or '
                            '5 characters'})

    def validate_login(self, user_data, user_name, password):

        if not user_data:
            return jsonify({'status': 400,
                            'message': 'All fields are required'})

        if not user_name or user_name == "":
            return jsonify({'status': 400,
                            'message': 'Username can not be empty'})
        if not isinstance(user_name, str):
            return jsonify({'status': 400,
                            'message': 'User name should be a string'})

        if not user_name.isalpha():
            return jsonify({'status': 400,
                            'message': 'User name should be '
                            'alphabetical letters'})

        if not user_name or user_name.strip() == "":
            return jsonify({'status': 400,
                            'message': 'User name should be filled'})

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
        if not order_data:
            return jsonify({'status': 400,
                            'message': 'Please fill all the feilds'})

        if not user_id or user_id == "":
            return jsonify({'status': 400,
                            'message': 'Oops! fill in user_id '
                            'and should be an integer.'})

        # if not isinstance(user_id, int) or user_id < 1:
        #     return jsonify({'status': 400,
        #                     'message': 'sorry! the user id '
        #                     'must be an integer > 0'})

        if type(user_id) != int or user_id == 0:
            return jsonify({'status': 400,
                            'message': 'sorry! the user id '
                            'must be an integer > 0'})

        if not user_name or user_name == "":
            return jsonify({'status': 400,
                            'message': 'Username can not be '
                            'an empty string.'})

        if type(user_name) == int or len(user_name) <= 5:
            return jsonify({'status': 400,
                            'message': 'Username must be more '
                            'than 5 letters.'})

        if not contact or contact == "":
            return jsonify({'status': 400,
                            'message': 'Contact is required '
                            'it should not be blank.'})

        # if not isinstance(contact, int) or user_id < 1:
        #     return jsonify({'status': 400,
        #                     'message': 'Contact should be an interger '
        #                     'of 7 to 15 digits.'})

        if type(contact) != int:
            return jsonify({'status': 400,
                            'message': 'Contact should be an interger '
                            'of 7 to 15 digits.'})

        if not pickup_location or pickup_location.isspace():
            return jsonify({'status': 400,
                            'message': 'Pickup location can not be '
                            'an empty string.'})

        if not destination or destination.isspace():
            return jsonify({'status': 400,
                            'message': 'Please! the destination '
                            'can no be empty.'})

        if type(destination) == int or len(destination) <= 4:
            return jsonify({'status': 400,
                            'message': 'Destination must have '
                            'atleast 4 letters.'})

        if not weight:
            return jsonify({'status': 400,
                            'message': 'Please the weight is required.'})

        if not isinstance(weight, int) or weight < 1.0:
            return jsonify({'status': 400,
                            'message': 'sorry! the weight '
                            'must be an integer > 0'})
        # if type(weight) != int:
        #     return jsonify({'status': 400,
        #                     'message': 'Sorry! the weight should be '
        #                     'an integer > 0.'})

        if not price:
            return jsonify({'status': 400,
                            'message': 'Please the price is required.'})

        if type(price) != int:
            return jsonify({'status': 400,
                            'message': 'Please! the price is '
                            'required as an integer.'})

        if not status or status == "":
            return jsonify({'status': 400,
                            'message': 'Status can be either pending, '
                            'delivered or cancelled.'})

        if not status.isalpha():
            return jsonify({'status': 400,
                            'message': 'Status should be '
                            'alphabetical letters'})

        if not isinstance(status, str):
            return jsonify({'status': 400,
                            'message': 'The status should be a string'})

    def validate_cancel_order(self, order_data, status):
        if not order_data or order_data == "":
            return jsonify({'status': 400,
                            'message': 'Please fill all the '
                            'required feilds'})

        if not status or status == " ":
            return jsonify({'status': 400,
                            'message': 'Please fill in the status '
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
        if not order_data:
            return jsonify({'status': 400,
                            'message': 'Please fill the required feilds'})
        if not status:
            return jsonify({'status': 400,
                            'message': 'Please fill in the status '
                            'of the order'})
                    
