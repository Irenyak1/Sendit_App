
import unittest
import json
from api.routes import app


class BaseTestCase(unittest.TestCase):
    """
    Base class for carrying out all tests.
    It defines a common 'setUp'
    method that defines the test client used
    in the various tests of the application.
    """
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

    def signup(self, user_name="irenyak", email="gigalasl@gmail.com",
               password="gigals", role="user"):

        """
        Method for signing up a user with dummy data
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

    def signup_admin(self, user_name="admin",
                     email="administrator@gmail.com",
                     password="admin123", role="admin"):
        """
        Method for signing up an admin with dummy data
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
        Method for logging in a user 
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

    def login_admin(self, user_name, password):
        """
        Method for logging in an admin
        """
        self.signup_admin()
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

    def get_admin_token(self, user_name="admin", password="admin123"):
        """
        Returns admin token
        """
        response = self.login_admin(user_name, password)
        token = json.loads(response.data.decode())['token']
        return token

    def get_user_token(self, user_name="irenyak", password="gigals"):
        """
        Returns a user token
        """
        response = self.login_user(user_name, password)
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

    def cancel_an_order(self, status="cancelled"):

        """
        Method for cancelling a delivery order with dummy data
        """
        return self.test_client.put(
            '/api/v1/orders/1/cancel',
            data=json.dumps(dict(
                status=status
            )
            ),
            content_type='application/json'
        )

    def test_get_index_page(self):
        """ Tests the api to return the index page"""
        with self.test_client:
            response = self.test_client.get('/api/v1/')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'You are most welcome to '
                                              'our home page')
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    # def test_get_all_users_when_userslist_is_empty(self):
    #   """ Tests the api to return all users when there are no users"""
    #     with self.test_client:
    #         response = self.test_client.get('/api/v1/users')
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'There are no users yet')
    #         self.assertEqual(data['status'], 400)
    #         self.assertEqual(response.status_code, 200)

    # def test_get_a_single_user_while_userslist_is_empty(self):
    #   """ Tests the api to return a single user when there are no users"""
    #     with self.test_client:
    #         response = self.test_client.get('/api/v1/users/1')
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'No users to display')
    #         self.assertEqual(data['status'], 400)
    #         self.assertEqual(response.status_code, 200)

    def test_signup(self):
        """ Tests the api to signup a user"""
        with self.test_client:
            response = self.signup("mexien", "mexien@gmail.com",
                                   "gooose", "user")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Thank you for signing up')
            self.assertEqual(data['status'], 201)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_without_user_data(self):
        """ Tests the api to signup a user without user data"""
        test_new_user = {}
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please fill all the feilds')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_with_username_not_a_string(self):
        """ Tests the api to signup a user with user name not a string"""
        test_new_user = {
            "user_name": 12234,
            "email": "gonehome@gmail.com",
            "password": "giagllls",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'User name must be a string')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_with_username_not_alphabetical(self):
        """ Tests the api to signup a user with user name not a letter"""
        test_new_user = {
            "user_name": "12234888",
            "email": "gigalasl@gmail.com",
            "password": "gigals",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'User name should be '
                                              'alphabetical letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_with_username_length_lessthan_five(self):
        """
        Tests the api to signup a user with username
        length less than five
        """
        test_new_user = {
            "user_name": "iren",
            "email": "gigalasl@gmail.com",
            "password": "gigals",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Username must be a string of '
                                              'at least 5 characters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_without_email(self):
        """ Tests the api to signup a user without email"""
        test_new_user = {
            "user_name": "irenyak",
            "email": "",
            "password": "gigals",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please email is required')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_with_wrong_email(self):
        """ Tests the api to signup a user with wrong email"""
        test_new_user = {
            "user_name": "jungleboot",
            "email": "alhdlgh?&&gmail.com",
            "password": "gigals",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please enter a valid email')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 400)

    def test_signup_user_without_password(self):
        """ Tests the api to signup a user without password"""
        test_new_user = {
            "user_name": "chessboard",
            "email": "chessboard@gmail.com",
            "password": "",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Password should be filled')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_with_length_of_password_lessthan_six(self):
        """
        Tests the api to signup a user with password
        length less than six
        """
        test_new_user = {
            "user_name": "jungles",
            "email": "jungles@gmail.com",
            "password": "giga",
            "role": "user"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'sorry! password must be '
                                              'at least 6 characters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_user_without_role(self):
        """ Tests the api to signup a user without role"""
        test_new_user = {
            "user_name": "football",
            "email": "football@gmail.com",
            "password": "gigals",
            "role": ""
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Role must be filled as '
                                              'user or admin')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_signup_with_role_not_admin_or_user(self):
        """
        Tests the api to signup a user with role
        other than admin or user
        """
        test_new_user = {
            "user_name": "smoothies",
            "email": "smoothies@gmail.com",
            "password": "gigals",
            "role": "admins"
        }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=test_new_user)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Role must be either user '
                                              'or admin')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_admin(self):
        """ Tests the api to login admin"""
        with self.test_client:
            response = self.login_admin("admin", "admin123")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Welcome admin')
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        """ Tests the api to login user"""
        with self.test_client:
            response = self.signup("irenyak", "gigalasl@gmail.com",
                                   "gigals", 'user')
            response = self.login_user("irenyak", "gigals")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'You have successfully '
                                              'logged in')
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_login_without_user_data(self):
        """ Tests the api to login user without user data"""
        login_details = {}

        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'All fields are required')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_without_user_name(self):
        """ Tests the api to login user without user name"""
        login_details = {
            "user_name": "",
            "password": "gigals"
        }

        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Username can not be empty')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_with_user_name_not_a_string(self):
        """ Tests the api to login user with user name not a string"""
        login_details = {
            "user_name": 123344,
            "password": "gigals"
        }

        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'User name should be a string')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_with_user_name_not_alphabetical(self):
        """ Tests the api to login user with user name not alphabetical"""
        login_details = {
            "user_name": "123344",
            "password": "gigals"
        }

        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'User name should be '
                                              'alphabetical letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_with_user_name_length_less_than_five(self):
        """ Tests the api to login user with user name not a string"""
        login_details = {
            "user_name": "iren",
            "password": "gigals"
        }

        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Username must be a string of '
                                              'at least 5 characters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_user_with_wrong_credentials(self):
        """ Tests the api to login user with user with wrong credentials"""
        new_user = {
                "user_name": "checked",
                "email": "checked@gmail.com",
                "password": "google",
                "role": "user"
            }

        logins = {
                "user_name": "major",
                "password": "badman"
            }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/signup',
                                             json=new_user)
            response = self.test_client.post('/api/v1/auth/login',
                                             json=logins)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Username or password did '
                                              'not match any user')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_user_without_password(self):
        """ Tests the api to login user without password"""
        login_details = {
                "user_name": "irenyak",
                "password": ""
            }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Fill in the password')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_login_user_with_password_length_less_than_five(self):
        """ Tests the api to login user with password length less than five"""
        login_details = {
                "user_name": "irenyak",
                "password": "giga"
            }
        with self.test_client:
            response = self.test_client.post('/api/v1/auth/login',
                                             json=login_details)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Password must be of '
                                              'at least 6 characters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        """ Tests the api to retrieve all users"""
        with self.test_client:
            response = self.signup("jammie", "jammie@gmail.com",
                                   "wisegal", "user")
            response = self.test_client.get('/api/v1/users')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_get_a_single_user(self):
        """ Tests the api to retrieve a single user"""
        with self.test_client:
            response = self.signup("humane", "jammiee@gmail.com",
                                   "wisegals", "user")
            response = self.test_client.get('/api/v1/users/1')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_get_a_non_existent_user(self):
        """ Tests the api to return a non-existent user"""
        with self.test_client:
            response = self.signup("kampala", "kampala@gmail.com",
                                   "cityland", "user")
            response = self.test_client.get('/api/v1/users/100')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'There is no such user '
                                              'in the list')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_token(self):
        """Tests api to create a delivery order without authorization"""
        with self.test_client:
            response = self.create_order(1, "mexien", 12345678, "Citysquare",
                                            "Gayaza", 10, 20000, "pending")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)

    def test_create_order_with_token(self):
        """Tests api to create a delivery order with authorization"""
        with self.test_client:
            response = self.test_client.post('/api/v1/orders',
                                            json=self.test_create_order,
                                            content_type='application/json',
                                            headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Delivery order created!')
            self.assertEqual(data['status'], 201)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_order_data(self):
        """Tests api to create a delivery order without order data"""
        test_create_order = {}
        with self.test_client:
            """ Test create order without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test create order with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please fill in order data')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_user_id(self):
        """Tests api to create a delivery order without user id"""
        test_create_order = {
            "user_id": 0,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """ Test without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Oops! fill in user_id '
                                              'and should be an integer')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_user_id_not_integer(self):
        """Tests api to create a delivery order with user id not an integer"""
        test_create_order = {
            "user_id": "1",
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'sorry! the user id '
                                              'must be an integer')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_user_id_less_than_1(self):
        """Tests api to create a delivery order with user id less than 1"""
        test_create_order = {
            "user_id": -1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """ Test without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'sorry! the user id '
                                              'can not be less than 1')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_username_not_string(self):
        """Tests api to create a delivery order with username not string"""
        test_create_order = {
            "user_id": 1,
            "user_name": 1233555,
            "contact": 234545678,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'User name must be a string')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_username_not_alphabetical(self):
        """
        Tests api to create a delivery order with
        user name not alphabetical
        """
        test_create_order = {
            "user_id": 1,
            "user_name": "&%#%%%78",
            "contact": 234545678,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'User name must be '
                                              'alphabetical letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_username_length_less_than_five(self):
        """
        Tests api to create a delivery order with username
        length less than 5
        """
        test_create_order = {
            "user_id": 1,
            "user_name": "iren",
            "contact": 234545678,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Username should be a string of '
                                              'at least 5 characters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_contact(self):
        """Tests api to create a delivery order without contact"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 0,
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Contact is required '
                                              'it should not be blank')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_if_contact_is_not_integer(self):
        """Tests api to create a delivery order with contact not an integer"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": "98798787",
            "pickup_location": "City square",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Contact should be an interger '
                                              'of 7 to 15 digits')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_pickup_location_is_missing(self):
        """Tests api to create a delivery order without pickup location"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Pickup location can not be '
                                              'an empty string')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_pickup_location_is_not_string(self):
        """Tests api to create a delivery order with pickup location not a string"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": 8788899390,
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Pickup location must be '
                                              'a string')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_pickup_location_is_not_alphabetical_letters(self):
        """Tests api to create a delivery order with pickup location not alphabetical"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "#$#%$#%^$#",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Pickup location must be '
                                              'alphabetical letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_pickup_location_less_than_4_letters(self):
        """Tests api to create a delivery order with pickup location less than 4 letters"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gul",
            "destination": "Gayaza",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Pickup location must have '
                                              'at least 4 letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_destination(self):
        """Tests api to create a delivery order without destination"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please! the destination '
                                              'can not be empty')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_destination_not_string(self):
        """Tests api to create a delivery order with destination not string"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": 897654777,
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Fill destination as a string')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_destination_alphabetical_letters(self):
        """Tests api to create a delivery order with destination not alphabetical"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "#$#%^&*$%",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Fill destination as '
                                              'alphabetical letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)


    def test_length_of_destination_lessthan_4letters(self):
        """Tests api to create a delivery order with destination length less than 4"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kam",
            "weight": 10,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Destination must have '
                                              'atleast 4 letters')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_weight(self):
        """Tests api to create a delivery order without weight"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": 0,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please the weight is required')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_weight_not_an_integer(self):
        """Tests api to create a delivery order with weight not integer"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": "ten",
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'sorry! the weight '
                                              'must be an integer > 0')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_weight_is_lessthan_1(self):
        """Tests api to create a delivery order with weight less than 1"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": -30,
            "price": 20000,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'sorry! the weight '
                                              'must be greater than 0')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_price(self):
        """Tests api to create a delivery order without price"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": 30,
            "price": 0,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please the price should '
                                              'be filled')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_price_is_not_integer(self):
        """Tests api to create a delivery order with price not integer"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": 30,
            "price": "10000",
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please! the price is '
                                              'required as an integer')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_price_is_lessthan_1(self):
        """Tests api to create a delivery order with price less than 1"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": 30,
            "price": -10,
            "status": "pending"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'The price can not be '
                                              'less than 1')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_create_order_without_status(self):
        """Tests api to create a delivery order without status"""
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": 30,
            "price": 20000,
            "status": ""
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=test_create_order,
                                             content_type='application/json',
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please fill in the status it can not be blank')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_order_with_status_other_than_pending_delivered_or_cancelled(self):
        """Tests api to create a delivery order with status
            otherthan  pending, delivered or cancelled
        """
        test_create_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "kampala",
            "weight": 30,
            "price": 20000,
            "status": "handled"
        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.post('/api/v1/orders',
                                            json=test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                            json=test_create_order,
                                            content_type='application/json',
                                            headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Status must be a string as '
                                              'either pending, delivered '
                                              'or cancelled')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_get_all_orders_when_orders_list_is_empty(self):
        """Tests api to retrieve all orders when orders list is empty"""
        with self.test_client:
            """Test this without token"""
            response = self.test_client.get('/api/v1/orders')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            # """Test this with token"""
            # response = self.test_client.get('/api/v1/orders',
            #                                  content_type='application/json',
            #                                  headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            # data = json.loads(response.data.decode())
            # self.assertEqual(data['message'], 'There are no delivery '
            #                                   'orders yet')
            # self.assertEqual(data['status'], 400)
            # self.assertEqual(response.status_code, 200)

    def test_get_an_order_when_orders_list_isempty(self):
        """Tests api to retrieve a delivery order when order list is empty"""
        with self.test_client:
            """Test this without token"""
            response = self.test_client.get('/api/v1/orders/1')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)

            # """Test this with token"""
            # response = self.test_client.get('/api/v1/orders/1',
            #                                  content_type='application/json',
            #                                  headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            # data = json.loads(response.data)
            # self.assertEqual(data['message'], 'You have no orders yet')
            # self.assertEqual(data['status'], 400)
            # self.assertEqual(response.status_code, 200)

    def test_get_all_orders(self):
        """Tests api to retrieve all orders made"""
        with self.test_client:
            """Test this without token"""
            response = self.test_client.get('/api/v1/orders')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """Test this with token"""
            response = self.test_client.get('/api/v1/orders',
                                            json=self.test_create_order,
                                            content_type='application/json',
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['orders_list'][0]['contact'], 234545678)
            self.assertEqual(data['orders_list'][0]['destination'], "Gayaza")

    def test_get_a_delivery_order(self):
        """Tests api to retrieve a single order"""
        with self.test_client:
            """Test without token"""
            response = self.test_client.get('/api/v1/orders/1',
                                             json=self.test_create_order)
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 401)
            self.assertEqual(data['message'], 'Please provide Token')
            self.assertEqual(response.status_code, 200)

            """Test with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=self.test_create_order,
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            self.assertEqual(data['status'], 201)
            response = self.test_client.get('/api/v1/orders/1',
                                            json=self.test_create_order,
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_get_a_nonexistent_order(self):
        """Tests api to retrieve a non-existent order"""
        with self.test_client:
            """Test this without token"""
            response = self.test_client.get('/api/v1/orders/100')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Please provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)

            """ Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=self.test_create_order,
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            self.assertEqual(data['status'], 201)
            response = self.test_client.get('/api/v1/orders/100',
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'There is no such delivery '
                                              'order in the list')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_get_a_delivery_order_by_a_user(self):
        """Tests api to retrieve an order by a specific user"""
        with self.test_client:
            """Test this without token"""
            response = self.test_client.get('/api/v1/orders/users/1/1')
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide Token')
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)

            """ Test this with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=self.test_create_order,
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            self.assertEqual(data['status'], 201)
            response = self.test_client.get('/api/v1/orders/users/1/1',
                                            headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)

    def test_cancel_an_order(self):
        """Tests api to cancel a pending order"""
        with self.test_client:
            """Test this without token"""
            response = self.cancel_an_order("cancelled")
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Please provide Token")
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test cancel order when order list is empty with token"""
            response = self.test_client.put('/api/v1/orders/1/cancel',
                                            json={'status': 'cancelled'},
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'There are no orders in the list yet')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)
            """Test cancel order with token"""
            response = self.test_client.post('/api/v1/orders',
                                             json=self.test_create_order,
                                             headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(200, response.status_code)
            self.assertEqual(data['status'], 201)
            response = self.test_client.put('/api/v1/orders/1/cancel',
                                            json={'status': 'cancelled'}, 
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Delivery order has '
                                              'been cancelled')
            self.assertEqual(data['status'], 200)
            self.assertEqual(response.status_code, 200)
            """ Test cancel non-existent user with token"""
            response = self.test_client.put('/api/v1/orders/100/cancel',
                                            json={'status': 'cancelled'},
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'The order has not been found')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)

    def test_cancel_an_order_by_a_user(self):
        """Tests api to cancel a pending order by a specific user"""
        with self.test_client:
            """Test cancel_an_order_by_a_user without token"""
            response = self.test_client.put('/api/v1/orders/users/1/1/cancel',
                                              json={'status': 'cancelled'})                              
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Provide Token")
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            # """ Test cancel_an_order_by_a_user when order list is empty with token"""
            # response = self.test_client.put('/api/v1/orders/users/1/1/cancel',
            #                                 json={'status': 'cancelled'},
            #                                  headers=dict(Authorization='Bearer ' + self.get_user_token()))
            # data = json.loads(response.data.decode())
            # self.assertEqual(data['message'], 'No delivery orders to cancel')
            # self.assertEqual(data['status'], 400)
            # self.assertEqual(response.status_code, 200)
    #         """Test cancel_an_order_by_a_user with token"""
    #         response = self.signup("marianah", "marianah@gmail.com", "bubbles", "user")
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['status'], 201)
    #         self.assertEqual(response.status_code, 200)
    #         response = self.test_client.post('/api/v1/orders',
    #                                          json=self.test_create_order,
    #                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(200, response.status_code)
    #         self.assertEqual(data['status'], 201)
    #         response = self.test_client.put('/api/v1/orders/users/1/1/cancel',
    #                                         json={'status': 'cancelled'},
    #                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'Pending order by the user '
    #                                           'has been cancelled')
    #         self.assertEqual(data['status'], 200)
    #         self.assertEqual(response.status_code, 200)
    #         """ Test cancel non-existent order with token"""
    #         response = self.test_client.put('/api/v1/orders/users/10/30/cancel',
    #                                         json={'status': 'cancelled'},
    #                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'The order is not found in the '
    #                                           'orders list or the user does not exist')
    #         self.assertEqual(data['status'], 400)
    #         self.assertEqual(response.status_code, 200)
    
    def test_cancel_all_orders_by_user(self):
        """Tests api to cancel all pending orders by a specific user"""
        with self.test_client:
            """Test cancel all orders by user without token"""
            response = self.test_client.put('/api/v1/orders/users/1/cancel_all',
                                            json={'status': 'cancelled'})
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Provide Token")
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test test_cancel_all_orders_by_user when order list is empty with token"""
            response = self.test_client.put('/api/v1/orders/users/1/cancel_all',
                                            json={'status': 'cancelled'},
                                            headers=dict(Authorization='Bearer ' + self.get_user_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'No orders to cancel')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)
    #         """Test test_cancel_all_orders_by_user with token"""
    #         response = self.signup("marianah", "marianah@gmail.com", "bubbles", "user")
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['status'], 201)
    #         self.assertEqual(response.status_code, 200)
    #         response = self.test_client.post('/api/v1/orders',
    #                                          json=self.test_create_order,
    #                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(200, response.status_code)
    #         self.assertEqual(data['status'], 201)
    #         response = self.test_client.put('/api/v1/orders/users/1/cancel_all',
    #                                         json={'status': 'cancelled'},
    #                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'All pending orders by the user '
    #                                           'have been cancelled')
    #         self.assertEqual(data['status'], 200)
    #         self.assertEqual(response.status_code, 200)
    #         """ Test cancel non-existent orders with token"""
    #         response = self.test_client.put('/api/v1/orders/users/100/cancel_all',
    #                                         json={'status': 'cancelled'},
    #                                          headers=dict(Authorization='Bearer ' + self.get_user_token()))
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(data['message'], 'User has no orders yet or user does not exist')
    #         self.assertEqual(data['status'], 400)
    #         self.assertEqual(response.status_code, 200)

    def test_cancel_all_orders(self):
        """Tests api to cancel all pending orders"""
        test_order = {
            "user_id": 1,
            "user_name": "irenyak",
            "contact": 234545678,
            "pickup_location": "gulu",
            "destination": "",
            "weight": 10,
            "price": 20000,
            "status": "Delivered"

        }
        with self.test_client:
            """Test this without token"""
            response = self.test_client.put('/api/v1/orders/cancel',
                                            json={'status': 'cancelled'})
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], "Please provide Token")
            self.assertEqual(data['status'], 401)
            self.assertEqual(response.status_code, 200)
            """ Test cancel all orders when order list is empty with token"""
            response = self.test_client.put('/api/v1/orders/cancel',
                                            json={'status': 'cancelled'},
                                            headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'There are no delivery orders to cancel')
            self.assertEqual(data['status'], 400)
            self.assertEqual(response.status_code, 200)
            # """Test cancel all orders with token"""
            # response = self.test_client.post('/api/v1/orders',
            #                                  json=self.test_create_order,
            #                                  headers=dict(Authorization='Bearer ' + self.get_user_token()))
            # data = json.loads(response.data.decode())
            # self.assertEqual(200, response.status_code)
            # self.assertEqual(data['status'], 201)
            # response = self.test_client.put('/api/v1/orders/cancel',
            #                                 json={'status': 'cancelled'}, 
            #                                  headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            # data = json.loads(response.data.decode())
            # self.assertEqual(data['message'], 'All pending orders have '
            #                                   'been cancelled')
            # self.assertEqual(data['status'], 200)
            # self.assertEqual(response.status_code, 200)
            # """ Test cancel orders which are not pending with token"""
            # response = self.test_client.post('/api/v1/orders',
            #                                  json=test_order,
            #                                  headers=dict(Authorization='Bearer ' + self.get_user_token()))
            # data = json.loads(response.data.decode())
            # self.assertEqual(200, response.status_code)
            # self.assertEqual(data['status'], 201)
            # response = self.test_client.put('/api/v1/orders/cancel',
            #                                 json={'status': 'cancelled'},
            #                                  headers=dict(Authorization='Bearer ' + self.get_admin_token()))
            # data = json.loads(response.data.decode())
            # self.assertEqual(data['message'], 'The orders can not be cancelled')
            # self.assertEqual(data['status'], 400)
            # self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
