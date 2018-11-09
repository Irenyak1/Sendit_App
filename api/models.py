from flask import Flask, request, jsonify, make_response


def get_index_page():
    return "You are most welcome to our home page"

""" This is a global variable called USERS """
USERS = [{"username": "admin", "password": "admin", "role": "admin"},
         {"username": "Maxie", "password": "elite", "role": "user"}]


class User:
    """
    This class defines the user in terms of
    the username, password and user_role.
    """

    user_role = ""

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def login(self):
        """ This method allows the user to login after cross checking their
            username, password and user role
        """
        for user in USERS:
            if user['username'] == self.username and user['password'] == self.password and user['role'] == self.role:
                User.user_role = self.role
        return self.user_role
