
import unittest
import json
from api.views import app
# import unittest
# from flask import json
# from api.models import User, Order
# from api.views import app
# # from tests.get_token import GetToken
# from api.auth import *
# from api.controllers import User_Controller


class BaseTestCase(unittest.TestCase):
    test_create_order = {
        "user_id": 1,
        "user_name": "irenyak",
        "contact": 234545678,
        "pickup_location": "Kampala",
        "destination": "Gayaza",
        "weight": 10,
        "price": 20000,
        "status": "pending"
    }

    def setUp(self):

        self.test_client = app.test_client()

    def signup(self, user_name="irenyak", email="gigalasl@gmail.com", password="gigals", role="user"):

        """
        Method for registering a user with dummy data
        """
        return self.test_client.post(
            'api/v1/auth/signup',
            data=json.dumps(dict(
                user_name=user_name,
                email=email,
                password=password,
                role=role
            )
            ),
            content_type='application/json'
        )

    def login_user(self, user_name, password):
        """
        Method for logging a user with dummy data
        """
        self.signup()
        return self.test_client.post(
            'api/v1/auth/login',
            data=json.dumps(
                dict(
                    user_name=user_name,
                    password=password
                )
            ),
            content_type='application/json'
        )

    def get_user_token(self, user_name="irenyak", password="gigals"):
        """
        Returns a user token
        """
        response = self.login_user(user_name, password)
        token = json.loads(response.data.decode())['token']
        return token
    
    def get_admin_token(self, user_name="admin", password="admin123"):
        """
        Returns a user token
        """
        response = self.login_user("admin", "admin123")
        token = json.loads(response.data.decode())['token']
        return token

    def create_order(self, user_id=1, user_name="mexien", contact=12345678,
                     pickup_location="Citysquare", destination="Gayaza",
                     weight=10,  price=20000, status="pending"):

        """
        Method for creating a delivery order with dummy data
        """
        return self.test_client.post(
            '/api/v1/orders',
            data=json.dumps(dict(
                user_id=user_id,
                user_name=user_name,
                contact=contact,
                pickup_location=pickup_location,
                destination=destination,
                weight=weight,
                price=price,
                status=status
            )
            ),
            content_type='application/json'
        )
    
    def cancel_an_order(self, order_id=1):
        
        """
        Method for cancelling a delivery order with dummy data
        """
        return self.test_client.put(
            '/api/v1/orders/1/cancel',
            data=json.dumps(dict(
                order_id=order_id
            )
            ),
            content_type='application/json'
        )

    # def test_index(self):
    #     # user_token = self.get_user_token()
    #     with self.test_client:
    #         response = self.test_client.get('/')
    #         # , content_type='application/json', headers=dict(Authorization='Bearer ' + user_token))
    #         # data = json.loads(response.data.decode())
    #         self.assertEqual(data.get('message'), 'You are most welcome to '
    #                                               'our home page')
    #         self.assertEqual(data['status'], 200)
    #         self.assertEqual(response.status_code, 200)
    
    def test_get_index_page(self):
        with self.test_client:
            response = self.test_client.get('/')
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'You are most welcome to '
                                              'our home page')
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    """Tests for user signup"""
    def test_signup(self):
        with self.test_client:
            response = self.signup("mexien", "mexien@gmail.com", "gooose", "user")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Thank you for signing up')
            self.assertEqual(data['status'], 201)
            self.assertEqual(response.status_code, 200)

    """Tests for user login"""
    def test_login(self):
        with self.test_client:
            response = self.signup("Irynah", "irynah@gmail.com",
                                   "chosen1", "user")
            response = self.login_user("Irynah", "chosen1")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'You have successfully '
                                              'logged in')
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    """Tests for retrieving user or users"""
    def test_get_all_users(self):
        with self.test_client:
            response = self.signup("jammie", "jammie@gmail.com", "wisegal", "user")
            response = self.test_client.get('/api/v1/users')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_get_a_single_user(self):
        with self.test_client:
            response = self.signup("humane", "jammiee@gmail.com", "wisegals", "user")
            response = self.test_client.get('/api/v1/users/1')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_get_a_non_existent_user(self):
        with self.test_client:
            response = self.signup("kampala", "kampala@gmail.com", "cityland", "user")
            response = self.test_client.get('/api/v1/users/100')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    """Tests for creating a delivery order"""
    def test_create_order_without_token(self):
        """Tests for creating a delivery order without token"""
        with self.test_client:
            response = self.create_order(1, "mexien", 12345678, "Citysquare",
                                            "Gayaza", 10, 20000, "pending")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)

    """Tests for creating a delivery order with token"""
    def test_create_order_with_token(self):
            with self.test_client:
                response = self.test_client.post('/api/v1/orders',
                                                json=self.test_create_order,
                                                content_type='application/json',
                                                headers=dict(Authorization='Bearer ' + self.get_user_token()))
                data = json.loads(response.data.decode())
                self.assertEqual(data['message'], 'Delivery order created!')
                self.assertEqual(data['status'], 201)
                self.assertEqual(response.status_code, 200)
    
    """Tests to cancel an order"""
    def test_cancel_an_order_without_token(self):
        """Test this without token"""
        # test_create_order = {
        #     "user_id": 1,
        #     "user_name": "irenyak",
        #     "contact": 234545678,
        #     "pickup_location": "gulu",
        #     "destination": "kampala",
        #     "weight": 30,
        #     "price": 20000,
        #     "status": "pending"
        # }
        with self.test_client:
            response = self.create_order(1, "mexien", 12345678, "Citysquare",
                                            "Gayaza", 10, 20000, "pending")
            response = self.cancel_an_order(1)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Please provide Token")
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
        
    # def test_cancel_an_order_with_token(self):
    #     """Test this with token"""
    #     with self.test_client:
    #         response = self.test_client.post('/api/v1/orders',
    #                                             json=self.test_create_order,
    #                                             content_type='application/json',
    #                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['status'], 201)
    #         response = self.test_client.put('/api/v1/orders/1/cancel',
    #                                         data={'status': 'cancelled'},
    #                                         content_type='application/json',
    #                                         headers=dict(Authorization='Bearer ' + self.get_admin_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'Delivery order has '
    #                                           'been cancelled')
    #         self.assertEqual(data['status'], 200)
    #         self.assertEqual(response.status_code, 200)

    # def test_cancel_order_with_token(self):
    #     """Test this with token"""
    #     with self.test_client:
    #         response = self.test_client.put('/api/v1/orders/1/cancel',
    #                                           json=self.test_create_order,
    #                                           content_type='application/json',
    #                                     
    #       headers=dict(Authorization='Bearer ' + self.get_admin_token()))
    #         response = self.test_client.get('/api/v1/orders/1')
    #         data = json.loads(response.data)
    #         self.assertEqual(data['message'], 'Token is missing')
    #         self.assertEqual(data['status'], 404)
    #         self.assertEqual(response.status_code, 200)
  
# bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
# import unittest
# from flask import json
# from api.models import User, Order
# from api.views import app
# # from tests.get_token import GetToken
# from api.auth import *
# from api.controllers import User_Controller


# class ApiTestCase(unittest.TestCase):

#     test_new_user = {
#             "user_name": "irenyak",
#             "email": "gigalasl@gmail.com",
#             "password": "gigals",
#             "role": "user"
#     }
#     test_create_order = {
#         "user_id": 1,
#         "user_name": "irenyak",
#         "contact": 234545678,
#         "pickup_location": "Kampala",
#         "destination": "Gayaza",
#         "weight": 10,
#         "price": 20000,
#         "status": "pending"
#     }

#     def setUp(self):
#         """Sets up the application configuration"""

#         self.test_client = app.test_client()

#         """Test for fetching index page"""


#     # def signup(self, user_name="irenyak", email="gigalasl@gmail.com",
#     #            password="gigals", role="user"):

#     #     """
#     #     Method for registering a user with dummy data
#     #     """
#     #     return self.test_client.post(
#     #         'api/v1/auth/signup',
#     #         data=json.dumps(dict(
#     #             user_name=user_name,
#     #             email=email,
#     #             password=password,
#     #             role=role
#     #         )
#     #         ),
#     #         content_type='application/json'
#     #     )

#     def login_user(self, user_name, password):
#         """
#         Method for logging a user with dummy data
#         """
#         User_Controller.signup_user(self)
#         return self.test_client.post(
#             'api/v1/auth/login',
#             data=json.dumps(
#                 dict(
#                     user_name=user_name,
#                     password=password
#                 )
#             ),
#             content_type='application/json'
#         )

#     def get_user_token(self, user_name="irenyak", password="gigals"):
#         """
#         Returns a user token
#         """
#         response = self.login_user(user_name, password)
#         users_token = json.loads(response.data.decode())['token']
#         return users_token

#     def get_admin_token(self, user_name="admin", password="admin123"):
#         """
#         Returns an admin token
#         """
#         response = self.login_user(user_name, password)
#         admins_token = json.loads(response.data.decode())['token']
#         return admins_token
       
#         """Tests for user signup"""
#     def test_signup_user(self):
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=self.test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Thank you for signing up')
#             self.assertEqual(data['status'], 201)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_without_user_data(self):
#         test_new_user = {}
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Please fill all the feilds')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_with_username_not_a_string(self):
#         test_new_user = {
#             "user_name": 12234,
#             "email": "gigalasl@gmail.com",
#             "password": "gigals",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'User name must be a string')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_with_username_not_alphabetical(self):
#         test_new_user = {
#             "user_name": "12234888",
#             "email": "gigalasl@gmail.com",
#             "password": "gigals",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'User name should be '
#                                               'alphabetical letters')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_without_username(self):
#         test_new_user = {
#             "user_name": "",
#             "email": "gigalasl@gmail.com",
#             "password": "gigals",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'User name should be '
#                                               'alphabetical letters')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_with_username_length_lessthan_five(self):
#         test_new_user = {
#             "user_name": "iren",
#             "email": "gigalasl@gmail.com",
#             "password": "gigals",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Username must be a string of '
#                                               'at least 5 characters')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_without_email(self):
#         test_new_user = {
#             "user_name": "irenyak",
#             "email": "",
#             "password": "gigals",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Please email is required')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_signup_user_with_wrong_email(self):
#         test_new_user = {
#             "user_name": "irenyak",
#             "email": "alhdlgh?&&gmail.com",
#             "password": "gigals",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Please enter a valid email')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 400)

#     def test_signup_user_without_password(self):
#             test_new_user = {
#                 "user_name": "irenyak",
#                 "email": "gigalasl@gmail.com",
#                 "password": "",
#                 "role": "user"
#             }
#             with self.test_client:
#                 response = self.test_client.post('/api/v1/auth/signup',
#                                                  json=test_new_user)
#                 data = json.loads(response.data)
#                 self.assertEqual(data['message'], 'Password should be filled')
#                 self.assertEqual(data['status'], 400)
#                 self.assertEqual(response.status_code, 200)

#     def test_signup_user_with_length_of_password_lessthan_six(self):
#             test_new_user = {
#                 "user_name": "irenyak",
#                 "email": "gigalasl@gmail.com",
#                 "password": "giga",
#                 "role": "user"
#             }
#             with self.test_client:
#                 response = self.test_client.post('/api/v1/auth/signup',
#                                                  json=test_new_user)
#                 data = json.loads(response.data)
#                 self.assertEqual(data['message'], 'sorry! password must be '
#                                                   'at least 6 characters')
#                 self.assertEqual(data['status'], 400)
#                 self.assertEqual(response.status_code, 200)

#     def test_signup_user_without_role(self):
#             test_new_user = {
#                 "user_name": "irenyak",
#                 "email": "gigalasl@gmail.com",
#                 "password": "gigals",
#                 "role": ""
#             }
#             with self.test_client:
#                 response = self.test_client.post('/api/v1/auth/signup',
#                                                  json=test_new_user)
#                 data = json.loads(response.data)
#                 self.assertEqual(data['message'], 'Role must be filled as '
#                                                   'user or admin')
#                 self.assertEqual(data['status'], 400)
#                 self.assertEqual(response.status_code, 200)

#     def test_signup_with_role_not_admin_or_user(self):
#         test_new_user = {
#             "user_name": "irenyak",
#             "email": "gigalasl@gmail.com",
#             "password": "gigals",
#             "role": "admins"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=test_new_user)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Role must be either user '
#                                               'or admin')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     """Tests for user login"""
    
#     def test_login_with_right_credentials(self):
#         new_user = {
#             "user_name": "mexien",
#             "email": "gigalasl@gmail.com",
#             "password": "goooose",
#             "role": "user"

#         }
#         login_details = {
#                 "user_name": "mexien",
#                 "password": "goooose"
#             }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=new_user)
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'You have successfully '
#                                               'logged in')
#             self.assertEqual(data['status'], 200)
#             self.assertEqual(response.status_code, 200)   

#     def test_login_without_user_data(self):
#         login_details = {}

#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'All fields are required')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_without_user_name(self):
#         login_details = {
#             "user_name": "",
#             "password": "gigals"
#         }

#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Username can not be empty')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_with_user_name_not_a_string(self):
#         login_details = {
#             "user_name": 123344,
#             "password": "gigals"
#         }

#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'User name should be a string')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_with_user_name_not_alphabetical(self):
#         login_details = {
#             "user_name": "123344",
#             "password": "gigals"
#         }

#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'User name should be '
#                                               'alphabetical letters')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_with_user_name_length_less_than_five(self):
#         login_details = {
#             "user_name": "iren",
#             "password": "gigals"
#         }

#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Username must be a string of '
#                                               'at least 5 characters')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_user_with_wrong_credentials(self):
#         login_details = {
#                 "user_name": "major",
#                 "password": "badman"
#             }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Username or password did '
#                                               'not match any user')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_user_without_password(self):
#         login_details = {
#                 "user_name": "irenyak",
#                 "password": ""
#             }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Fill in the password')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     def test_login_user_with_password_length_less_than_five(self):
#         login_details = {
#                 "user_name": "irenyak",
#                 "password": "giga"
#             }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/login',
#                                              json=login_details)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Password must be of '
#                                               'at least 6 characters')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     # """Tests for retrieving user or users"""
#     # def test_get_all_users_when_userslist_is_empty(self):
#     #     with self.test_client:
#     #         response = self.test_client.get('/api/v1/users')
#     #         data = json.loads(response.data)
#     #         self.assertEqual(data['message'], 'There are no users yet')
#     #         self.assertEqual(data['status'], 400)
#     #         self.assertEqual(response.status_code, 200)

#     # def test_get_a_single_user_while_userslist_is_empty(self):
#     #     with self.test_client:
#     #         response = self.test_client.get('/api/v1/users/1')
#     #         data = json.loads(response.data)
#     #         self.assertEqual(data['message'], 'No users to display')
#     #         self.assertEqual(data['status'], 400)
#     #         self.assertEqual(response.status_code, 200)

#     def test_get_all_users(self):
#         user = {
#             "user_name": "mamamia",
#             "email": "goodgal@gmail.com",
#             "password": "sleeky",
#             "role": "user"

#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=user)
#             response = self.test_client.get('/api/v1/users')
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 200)
#             self.assertEqual(response.status_code, 200)

    # def test_get_a_single_user(self):
    #     user = {
    #         "user_name": "mamamia",
    #         "email": "goodgal@gmail.com",
    #         "password": "sleeky",
    #         "role": "user"

    #     }
    #     with self.test_client:
    #         response = self.test_client.post('/api/v1/auth/signup',
    #                                          json=user)
    #         response = self.test_client.get('/api/v1/users/187')
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['status'], 200)
    #         self.assertEqual(response.status_code, 200)

#     def test_get_a_non_existent_user(self):
#         my_user = {
#             "user_name": "mexien",
#             "email": "gigalasl@gmail.com",
#             "password": "goooose",
#             "role": "user"
#         }
#         with self.test_client:
#             response = self.test_client.post('/api/v1/auth/signup',
#                                              json=my_user)
#             response = self.test_client.get('/api/v1/users/10')
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'There is no such user '
#                                               'in the list')
#             self.assertEqual(data['status'], 400)
#             self.assertEqual(response.status_code, 200)

#     """Tests for creating a delivery order"""
#     def test_create_delivery_orderwithout_token(self):
#         with self.test_client:
#             """Test for creating a delivery order without token"""
#             response = self.test_client.post('/api/v1/orders',
#                                              json=self.test_create_order)
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Provide Token')
#             self.assertEqual(data['status'], 401)
#             self.assertEqual(response.status_code, 200)
#             """Test for creating a delivery order without token"""
#             # users_token = self.get_user_token()
#             return self.test_client.post('/api/v1/orders',
#                                          json=self.test_create_order,
#                                          content_type='application/json',
#                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
#             data = json.loads(response.data)
#             self.assertEqual(data['message'], 'Delivery order created!')
#             self.assertEqual(data['status'], 201)
#             self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_order_data(self):
# #         test_create_order = {}
# #         with self.test_client:
# #             """ Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)

# #     #         # response = self.test_client.post('/api/v1/orders',
# #     #         #                                  json=test_create_order)
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['message'], 'Please fill in order data')
# #     #         # self.assertEqual(data['status'], 400)
# #     #         # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_user_id(self):
# #         test_create_order = {
# #             "user_id": 0,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)

# #     #         # response = self.test_client.post('/api/v1/orders',
# #     #         #                                  json=test_create_order)
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['message'], 'Oops! fill in user_id '
# #     #         #                                   'and should be an integer')
# #     #         # self.assertEqual(data['status'], 400)
# #     #         # self.assertEqual(response.status_code, 200)

# #     def test_user_id_not_integer(self):
# #         test_create_order = {
# #             "user_id": "1",
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #     #         # """" Test this with token"""
# #     #         # response = self.test_client.post('/api/v1/orders',
# #     #         #                                  json=test_create_order)
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['message'], 'sorry! the user id '
# #     #         #                                   'must be an integer')
# #     #         # self.assertEqual(data['status'], 400)
# #     #         # self.assertEqual(response.status_code, 200)

# #     def test_user_id_less_than_1(self):
# #         test_create_order = {
# #             "user_id": -1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """ Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'sorry! the user id '
# #             #                                   'can not be less than 1')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_username(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "",
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Username can not be '
# #             #                                   'an empty string')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_username_not_string(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": 1233555,
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'User name must be a string')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_username_not_alphabetical(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "&%#%%%78",
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'User name must be '
# #             #                                   'alphabetical letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_username_length_less_than_five(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "iren",
# #             "contact": 234545678,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Username should be a string of '
# #             #                                   'at least 5 characters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_contact(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 0,
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Contact is required '
# #             #                                   'it should not be blank')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_if_contact_is_not_integer(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": "98798787",
# #             "pickup_location": "City square",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Contact should be an interger '
# #             #                                   'of 7 to 15 digits')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_pickup_location_is_missing(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Pickup location can not be '
# #             #                                   'an empty string')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_pickup_location_is_not_string(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": 8788899390,
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Pickup location must be '
# #             #                                   'a string')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_pickup_location_is_not_alphabetical_letters(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "#$#%$#%^$#",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Pickup location must be '
# #             #                                   'alphabetical letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_pickup_location_less_than_4_letters(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gul",
# #             "destination": "Gayaza",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Pickup location must have '
# #             #                                   'at least 4 letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_destination(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Please! the destination '
# #             #                                   'can not be empty')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_destination_not_string(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": 897654777,
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Fill destination as a string')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_destination_alphabetical_letters(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "#$#%^&*$%",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Fill destination as '
# #             #                                   'alphabetical letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_length_of_destination_lessthan_4letters(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kam",
# #             "weight": 10,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Destination must have '
# #             #                                   'atleast 4 letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_weight(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 0,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Please the weight is required')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_weight_not_an_integer(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": "ten",
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'sorry! the weight '
# #             #                                   'must be an integer > 0')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_weight_is_lessthan_1(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": -30,
# #             "price": 20000,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'sorry! the weight '
# #             #                                   'must be greater than 0')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_price(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": 0,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Please the price should '
# #             #                                   'be filled')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_price_is_not_integer(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": "10000",
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Please! the price is '
# #             #                                   'required as an integer')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_price_is_lessthan_1(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": -10,
# #             "status": "pending"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'The price can not be '
# #             #                                   'less than 1')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_create_order_without_status(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": 20000,
# #             "status": ""
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Fill in the status as either '
# #             #                                   'pending, delivered or canceled')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_status_is_not_string(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": 20000,
# #             "status": 345678
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'The status should be a string')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_status_is_not_alphabetical_letters(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": 20000,
# #             "status": "#$$%^&*()"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Status should be '
# #             #                                   'alphabetical letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     def test_length_of_status_is_lessthan_4(self):
# #         test_create_order = {
# #             "user_id": 1,
# #             "user_name": "irenyak",
# #             "contact": 234545678,
# #             "pickup_location": "gulu",
# #             "destination": "kampala",
# #             "weight": 30,
# #             "price": 20000,
# #             "status": "pen"
# #         }
# #         with self.test_client:
# #             """Test this without token"""
# #             response = self.test_client.post('/api/v1/orders',
# #                                              json=self.test_create_order)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['message'], 'Provide Token')
# #             self.assertEqual(data['status'], 401)
# #             self.assertEqual(response.status_code, 200)
# #             # """Test this with token"""
# #             # response = self.test_client.post('/api/v1/orders',
# #             #                                  json=test_create_order)
# #             # data = json.loads(response.data)
# #             # self.assertEqual(data['message'], 'Fill the status as a string, '
# #             #                                   'of at least 4 letters')
# #             # self.assertEqual(data['status'], 400)
# #             # self.assertEqual(response.status_code, 200)

# #     # """Tests for retrieving an order or orders"""
# #     # def test_get_all_orders_when_orders_list_is_empty(self):
# #     #     with self.test_client:
# #     #         """Test this without token"""
# #     #         response = self.test_client.get('/api/v1/orders')
# #     #         data = json.loads(response.data)
# #     #         self.assertEqual(data['message'], 'Token is missing')
# #     #         self.assertEqual(data['status'], 404)
# #     #         self.assertEqual(response.status_code, 200)

# #     #         # """Test this without token"""
# #     #         # response = self.test_client.get('/api/v1/orders')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['message'], 'There are no delivery '
# #     #         #                                   'orders yet')
# #     #         # self.assertEqual(data['status'], 400)
# #     #         # self.assertEqual(response.status_code, 200)

# #     # def test_get_an_order_when_orders_list_isempty(self):
# #     #     with self.test_client:
# #     #         """Test this without token"""
# #     #         response = self.test_client.get('/api/v1/orders/1')
# #     #         data = json.loads(response.data)
# #     #         self.assertEqual(data['message'], 'Token is missing')
# #     #         self.assertEqual(data['status'], 404)
# #     #         self.assertEqual(response.status_code, 200)

# #     #         # # """Test this without token"""
# #     #         # response = self.test_client.get('/api/v1/orders/1')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['message'], 'You have no orders yet')
# #     #         # self.assertEqual(data['status'], 400)
# #     #         # self.assertEqual(response.status_code, 200)

# #     # def test_get_all_orders(self):
# #     #     test_create_order = {
# #     #         "user_id": 1,
# #     #         "user_name": "irenyak",
# #     #         "contact": 234545678,
# #     #         "pickup_location": "gulu",
# #     #         "destination": "kampala",
# #     #         "weight": 30,
# #     #         "price": 20000,
# #     #         "status": "pending"
# #     #     }
# #     #     with self.test_client:
# #     #         """Test this without token"""
# #     #         response = self.test_client.post('/api/v1/orders',
# #     #                                          json=test_create_order)
# #     #         response = self.test_client.get('/api/v1/orders')
# #     #         data = json.loads(response.data)
# #     #         self.assertEqual(data['message'], 'Token is missing')
# #     #         self.assertEqual(data['status'], 404)
# #     #         self.assertEqual(response.status_code, 200)

# #     #         # """Test this with token"""
# #     #         # response = self.test_client.post('/api/v1/orders',
# #     #         #                                  json=test_create_order)
# #     #         # response = self.test_client.get('/api/v1/orders')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['status'], 200)
# #     #         # self.assertEqual(response.status_code, 200)
# #     #         # self.assertEqual(data['orders_list'][0]['contact'], 234545678)
# #     #         # self.assertEqual(data['orders_list'][0]['destination'], "Gayaza")

# #     # def test_get_a_delivery_order(self):
# #     #     test_create_order = {
# #     #         "user_id": 1,
# #     #         "user_name": "irenyak",
# #     #         "contact": 234545678,
# #     #         "pickup_location": "Kampala",
# #     #         "destination": "Gayaza",
# #     #         "weight": 10,
# #     #         "price": 20000,
# #     #         "status": "pending"
# #     #     }
# #     #     with self.test_client:
# #     #         """Test this without token"""
# #     #         response = self.test_client.post('/api/v1/orders',
# #     #                                          json=test_create_order)
# #     #         response = self.test_client.get('/api/v1/orders')
# #     #         data = json.loads(response.data)
# #     #         self.assertEqual(data['message'], 'Token is missing')
# #     #         self.assertEqual(data['status'], 404)
# #     #         self.assertEqual(response.status_code, 200)

# #     #         # """Test this with token"""
# #     #         # response = self.test_client.post('/api/v1/orders',
# #     #         #                                  json=test_create_order,
# #     #         #                                  headers=dict(Authorization=GetToken.get_user_token()))
# #     #         # response = self.test_client.get('/api/v1/orders/1')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['status'], 200)
# #     #         # self.assertEqual(response.status_code, 200)

# #     # def test_get_a_nonexistent_order(self):
# #     #     test_create_order = {
# #     #         "user_id": 1,
# #     #         "user_name": "irenyak",
# #     #         "contact": 234545678,
# #     #         "pickup_location": "gulu",
# #     #         "destination": "kampala",
# #     #         "weight": 30,
# #     #         "price": 20000,
# #     #         "status": "pending"
# #     #     }
# #     #     with self.test_client:
# #     #         """Test this without token"""
# #     #         response = self.test_client.post('/api/v1/orders',
# #     #                                          json=test_create_order)
# #     #         response = self.test_client.get('/api/v1/orders')
# #     #         data = json.loads(response.data)
# #     #         self.assertEqual(data['message'], 'Token is missing')
# #     #         self.assertEqual(data['status'], 404)
# #     #         self.assertEqual(response.status_code, 200)
   
# #     #         # """ Test this with token"""
# #     #         # response = self.test_client.post('/api/v1/orders',
# #     #         #                                  json=test_create_order,
# #     #         #                                  headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
# #     #         # response = self.test_client.get('/api/v1/orders/7')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['message'], 'There is no such delivery '
# #     #         #                                   'order in the list')
# #     #         # self.assertEqual(data['status'], 400)
# #     #         # self.assertEqual(response.status_code, 200)

# #     # def test_get_a_delivery_order_by_a_user(self):
# #     #     test_create_order = {
# #     #         "user_id": 1,
# #     #         "user_name": "irenyak",
# #     #         "contact": 234545678,
# #     #         "pickup_location": "gulu",
# #     #         "destination": "kampala",
# #     #         "weight": 30,
# #     #         "price": 20000,
# #     #         "status": "pending"
# #     #     }
# #     #     with self.test_client:
# #     #         """Test this without token"""
# #     #         response = self.test_client.post('/api/v1/orders',
# #     #                                          json=test_create_order)
# #     #         response = self.test_client.get('/api/v1/orders/1')
# #     #         data = json.loads(response.data)
# #     #         self.assertEqual(data['message'], 'Token is missing')
# #     #         self.assertEqual(data['status'], 404)
# #     #         self.assertEqual(response.status_code, 200)

# #     #         # """Test this with token"""
# #     #         # response = self.test_client.post('/api/v1/orders/users/1',
# #     #         #                                  json=test_create_order)
# #     #         # response = self.test_client.get('/api/v1/orders/1')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['status'], 200)
# #     #         # self.assertEqual(response.status_code, 200)

        # """Tests to cancel an order"

# #     # def test_cancel_order(self):
# #     #     # test_create_order = {
# #     #     #     "user_id": 1,
# #     #     #     "user_name": "irenyak",
# #     #     #     "contact": 234545678,
# #     #     #     "pickup_location": "gulu",
# #     #     #     "destination": "kampala",
# #     #     #     "weight": 30,
# #     #     #     "price": 20000,
# #     #     #     "status": "pending"
# #     #     # }
# #     #     # with self.test_client:
# #     #     #     """Test this without token"""
# #     #     #     response = self.test_client.post('/api/v1/orders',
# #     #     #                                      json=test_create_order)
# #     #     #     response = self.test_client.get('/api/v1/orders/1')
# #     #     #     data = json.loads(response.data)
# #     #     #     self.assertEqual(data['message'], 'Token is missing')
# #     #     #     self.assertEqual(data['status'], 404)
# #     #     #     self.assertEqual(response.status_code, 200)
     
# #     #         # """Test this with token"""
# #     #         # response = self.test_client.post('/api/v1/orders/users/1',
# #     #         #                                  json=test_create_order)
# #     #         # response = self.test_client.get('/api/v1/orders/1')
# #     #         # data = json.loads(response.data)
# #     #         # self.assertEqual(data['status'], 200)
# #     #         # self.assertEqual(response.status_code, 200)

# #         def tearDown(self):
# #             pass





# # import unittest
# # import json
# # from api.views import app


# # class BaseTestCase(unittest.TestCase):
# # #     def create_app(self):
# # #         """
# # #         Create an instance of the app with the testing configuration
# # #         """
# # #         APP.config.from_object(app_config["testing"])
# # #         return APP

# #     def setUp(self):
# # #         """
# # #         Create the database and commits any changes made permanently
# # #         """
# #         # self.client = app.test_client(self)
# # #         DB.create_all()
# # #         DB.session.commit()
# #         self.test_client = app.test_client()
# #         # self.database = DatabaseConnection()
# #         # self.database.create_users_table()
# #         # self.database.create_incident_tables()

#     # def tearDown(self):
# #         """
# #         Drop the database data and remove session
# #         """
# #         DB.session.remove()
# #         DB.drop_all()
#         # self.database.cursor.execute("DROP TABLE incidents")
#         # self.database.cursor.execute("DROP TABLE users")

# #     def register_user(
# #             self,
# #             name="marie",
# #             email="marie@live.com",
# #             password="marie",
# #             is_admin="True"):
#     # def signup(self, user_name="irenyak", email="gigalasl@gmail.com", password="gigals", role="user"):

#     #     """
#     #     Method for registering a user with dummy data
#     #     """
#     #     return self.test_client.post(
#     #         'api/v1/auth/signup',
#     #         data=json.dumps(dict(
#     #             user_name=user_name,
#     #             email=email,
#     #             password=password,
#     #             role=role
#     #         )
#     #         ),
#     #         content_type='application/json'
#     #     )

#     # def login_user(self, user_name, password):
#     #     """
#     #     Method for logging a user with dummy data
#     #     """
#     #     self.signup()
#     #     return self.test_client.post(
#     #         'api/v1/auth/login',
#     #         data=json.dumps(
#     #             dict(
#     #                 user_name=user_name,
#     #                 password=password
#     #             )
#     #         ),
#     #         content_type='application/json'
#     #     )

#     # def get_token(self, user_name="irenyak", password="gigals"):
#     #     """
#     #     Returns a user token
#     #     """
#     #     response = self.login_user(user_name, password)
#     #     token = json.loads(response.data.decode())['token']
#     #     return token
       

#     # def test_index(self):
#     #     token = self.get_token()
#     #     # headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
#     #     return self.test_client.get('/', content_type = 'application/json', headers=dict(Authorization='Bearer ' + token))
   