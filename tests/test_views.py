import unittest
from flask import json
from api.models import User, Order
from api.views import app


# test_new_user = {
#      "user_name": "Irynah", 
#      "password": "gilgal",
#      "role": "user"
#     }


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        "Sets up the application configuration"

        self.test_client = app.test_client()


    """Test for fetching index page"""
    def test_get_index_page(self):
        with self.test_client:
            response = self.test_client.get('/')
            self.assertEqual(response.status_code, 200 )
            self.assertIn('You are most welcome to our home page', response.data.decode())    
    
    """Tests for user signup"""    
    def test_signup_user(self):
        with self.test_client:
            response = self.test_client.post('/api/v1/signup',
                                             content_type='application/json',
                                             data=json.dumps(dict(user_name="Irynah",
                                                                 email="gal@gmail.com",
                                                                 password="gilgal",
                                                                 role="admin")))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Thank you for signing up',
                          responseJson['message'])
    
    """Test for user login"""

    def test_login_user(self):
        with self.test_client:
            response = self.test_client.post('/api/v1/login',
                                                content_type='application/json',
                                                data=json.dumps(dict(username="Irynah",
                                                                     password="gilgal",
                                                                     role="admin")))
            self.assertEqual(response.status_code, 201)
            # responseJson = json.loads(response.data.decode())
            # self.assertIn(f"Welcome {role}, You are logged in",
                            # responseJson['message'])



    def test_if_order_data_is_empty(self):
        with self.test_client:
            User.role = 'user'
            response = self.test_client.post('/api/v1/orders', 
                                             content_type='application/json',
                                             data=json.dumps(dict()))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Please fill all the feilds',
                          responseJson['message'])

    # def test_if_user_id_is_empty(self):
    #     with self.test_client:
    #         User.role = 'user'
    #         response = self.test_client.post('/api/v1/orderss',
    #                                          content_type='application/json',
    #                                          data=json.dumps(dict(user_id=" ",
    #                                                               user_name="Irynah",
    #                                                               contact="8765436789",
    #                                                               pickup_location= "Namere",
    #                                                               destination= "Mukono",
    #                                                               weight=78,
    #                                                               price=25000)))
    #         self.assertEqual(response.status_code, 400)
    #         responseJson = json.loads(response.data.decode())
    #         self.assertIn('Oops! fill in user_id and should be an integer',
    #                       responseJson['message'])
    
    # def test_if_user_id_is_not_integer(self):
    #     with self.test_client:
    #         User.role = 'user'
    #         response = self.test_client.post('/api/v1/orderss',
    #                                          content_type='application/json',
    #                                          data=json.dumps(dict(user_id="h390",
    #                                                               user_name="Irynah",
    #                                                               contact="8765436789",
    #                                                               pickup_location= "Namere",
    #                                                               destination= "Mukono",
    #                                                               weight=78,
    #                                                               price=25000)))
    #         self.assertEqual(response.status_code, 400)
    #         responseJson = json.loads(response.data.decode())
    #         self.assertIn('sorry! the user_id must be an integer > 0',
    #                       responseJson['message'])

    # def tearDown(self):
    #     pass
