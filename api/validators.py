import re
from flask import jsonify

class Validators:

    def validate_signup(self, user_data, user_name, email, password, role ):

        if not user_data:
            return jsonify({'status':400, 'message': 'Please fill all the feilds'})
        
        # if not isinstance(user_name, str):
        #     return jsonify({'message': 'User name should be a string'}), 400
        
        if not user_name.isalpha():
            return jsonify({'status':400 ,'message': 'User name should be letters of the alphabet'})

        if not user_name or user_name.strip() == "":
            return jsonify({'message': 'User name should be filled'}), 400
        
        if type(user_name) == int or len(user_name) < 5:
            return jsonify({
                'message': 'Username must be a string of at least 5 characters'
            }), 400

        if not email or email.isspace():
            return jsonify({'status':400, 'message': 'Please email is required'})

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
