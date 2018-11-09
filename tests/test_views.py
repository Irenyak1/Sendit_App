import unittest
from flask import json
from api.views import app


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        "Sets up the application configuration"

        self.test_client = app.test_client()

    def tearDown(self):
        pass
