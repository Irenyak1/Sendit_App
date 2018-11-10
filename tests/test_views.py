import unittest
from flask import json
from api.models import User
from api.views import app


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        "Sets up the application configuration"

        self.test_client = app.test_client()

    def test_if_order_data_is_empty(self):
        with self.test_client:
            User.user_role = 'user'
            response = self.test_client.post('/api/v1/orders', content_type='application/json',
                                             data=json.dumps(dict()))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Please fill all the feilds',
                          responseJson['message'])

    
    
    def tearDown(self):
        pass
