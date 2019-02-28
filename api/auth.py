from functools import wraps
from flask import request, jsonify
import jwt
import datetime


adminkey = 'access'
userkey = 'nogo'


def admin_token(func):
    @wraps(func)
    def _verify(*args, **kwargs):
        admin_headers = request.headers.get('Authorization', '').split()
        try:
            admins_token = admin_headers[1]
            print(admins_token)
            # if not admins_token:
            #     error = jsonify({'status': 403,
            #                      'message': 'Token is missing'})
            data = jwt.decode(admins_token, "access")
            return func(*args, **kwargs)
        except IndexError:
            error = jsonify({'status': 401,
                             "message": "Please provide Token",
                             "authenticated": False})
        except jwt.DecodeError:
            error = jsonify({'status': 401,
                             "message": "Token Decode Failed!",
                            "authenticated": False})
        except jwt.ExpiredSignatureError:
            error = jsonify({'status': 401,
                             'message': 'Expired token. Please Log In again.',
                             'authenticated': False})
        except jwt.InvalidTokenError:
            error = jsonify({'status': 401,
                             'message': 'Invalid token. Please Log In again',
                             'authenticated': False})
        return error

    return _verify


def user_token(func):
    @wraps(func)
    def _verify(*args, **kwargs):
        user_headers = request.headers.get('Authorization', '').split()
        try:
            users_token = user_headers[1]
            print(users_token)
            # if not users_token:
            #     error = jsonify({'status': 403,
            #                     'message': 'Token not provided'})
            data = jwt.decode(users_token, "nogo")
            return func(*args, **kwargs)
        except IndexError:
            error = jsonify({'status': 401,
                             'message': 'Provide Token',
                             'authenticated': False})
        except jwt.DecodeError:
            error = jsonify({'status': 401,
                             'message': 'Token Decode Failed!',
                             'authenticated': False})
        except jwt.ExpiredSignatureError:
            error = jsonify({'status': 401,
                             'message': 'Expired token. Please Log In again.',
                             'authenticated': False})
        # except jwt.InvalidTokenError:
        #     error = jsonify({'status': 401,
        #                      'message': 'Invalid token. Please Log In again',
        #                      'authenticated': False})
        return error

    return _verify
