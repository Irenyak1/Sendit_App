import unittest
from flask import json
from api.models import User, Order
from api.views import app


class ApiTestCase(unittest.TestCase):

    test_new_user = {
        "user_name": "Irynah", 
        "email": "gal@gmail.com",
        "password": "gilgal",
        "role": "user"
    }

    def setUp(self):
        "Sets up the application configuration"

        self.test_client = app.test_client()

    """Test for fetching index page"""
    def test_get_index_page(self):
        with self.test_client:
            response = self.test_client.get('/')
            data = json.loads(response.data)
            self.assertEqual(data ['message'],'You are most welcome to our home page')
            self.assertEqual(data ['status'],200)
            self.assertEqual(response.status_code, 200 )
    
    
    """Tests for user signup"""    
    def test_signup_user(self):
        with self.test_client:
            response = self.test_client.post('/api/v1/signup', json = self.test_new_user)
            data = json.loads(response.data)
            self.assertEqual(data ['message'],'Thank you for signing up')
            self.assertEqual(data ['status'],201)
            self.assertEqual(response.status_code, 200 )
    
    def test_signup_user_without_user_data(self):
        test_new_user = {   }
        with self.test_client:
            response = self.test_client.post('/api/v1/signup', json = test_new_user)
            data = json.loads(response.data)
            self.assertEqual(data ['message'],'Please fill all the feilds')
            self.assertEqual(data ['status'],400)
            self.assertEqual(response.status_code, 200 )

    def test_signup_user_without_username(self):
        test_new_user = {
            "user_name": "", 
            "email": "gal@gmail.com",
            "password": "gilgal",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/signup', json = test_new_user)
            data = json.loads(response.data)
            self.assertEqual(data ['message'], 'User name should be '
                                               'alphabetical letters')
            self.assertEqual(data ['status'],400)
            self.assertEqual(response.status_code, 200 )

    def test_signup_user_without_email(self):
        
        test_new_user = {
            "user_name": "Irenyakss", 
            "email": "",
            "password": "gilgal",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/signup', json = test_new_user)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Please email is required')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_without_password(self):
            
            test_new_user = {
                "user_name": "Irenyakss", 
                "email": "galll@gmail.com",
                "password": "",
                "role": "user"
            }
            with self.test_client:
                response = self.test_client.post('/api/v1/signup',
                                                 json=test_new_user)
                data = json.loads(response.data)
                self.assertEqual(data['message'], 'Password should be filled')
                self.assertEqual(data['status'], 400)
                self.assertEqual(response.status_code, 200)

    def test_signup_user_without_role(self):
            
            test_new_user = {
                "user_name": "Irenyakss", 
                "email": "galll@gmail.com",
                "password": "gilgals",
                "role": ""
            }
            with self.test_client:
                response = self.test_client.post('/api/v1/signup',
                                                 json=test_new_user)
                data = json.loads(response.data)
                self.assertEqual(data['message'], 'sorry! the role should '
                                                  'be filled as either admin '
                                                  'or user')
                self.assertEqual(data['status'], 400)
                self.assertEqual(response.status_code, 200)
    
    # """Test for user login"""

    # def test_login_user(self):
    #     with self.test_client:
    #         response = self.test_client.post('/api/v1/login',
    #                                             content_type='application/json',
    #                                             data=json.dumps(dict(username="Irynah",
    #                                                                  password="gilgal",
    #                                                                  role="admin")))
    #         self.assertEqual(response.status_code, 201)
    #         responseJson = json.loads(response.data.decode())
    #         self.assertIn(f'Welcome {role}, You are logged in',
    #                         responseJson['message'])



    # def test_if_order_data_is_empty(self):
    #     with self.test_client:
    #         User.role = 'user'
    #         response = self.test_client.post('/api/v1/orders', 
    #                                          content_type='application/json',
    #                                          data=json.dumps(dict()))
    #         self.assertEqual(response.status_code, 400)
    #         responseJson = json.loads(response.data.decode())
    #         self.assertIn('Please fill all the feilds',
    #                       responseJson['message'])

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
