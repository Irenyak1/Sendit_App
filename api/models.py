
""" A global variable called USERS """
USERS = [{"user_name": "admin", "password": "admin", "role": "admin"},
         {"user_name": "Maxie", "password": "elite", "role": "user"}]
# This is a list that will store all the users


#  This defines the user class
class User:
    """
    This class defines the user in terms of
    the user_name, password and role.
    """
    role = ""

    def __init__(self, user_name, email, password, role, user_id):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role
        self.user_id = len(USERS) + 1

    def to_dict(self):
        user = {
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "user_id": self.user_id
        }

        return user

        
ORDERS = []
# This is a list that will store all the orders


# This defines the order class
class Order:
    """
    This class defines a parcel delivery order in terms of
    user_id, user_name, contact, pickup_location,
    destination, weight, price and order_id,
    """

    def __init__(self, user_id, user_name, contact,
                 pickup_location, destination, weight, price, order_id):
        self.user_id = user_id
        self.user_name = user_name
        self.contact = contact
        self.pickup_location = pickup_location
        self.destination = destination
        self.weight = weight
        self.price = price
        self.order_id = len(ORDERS) + 1

    def to_dict(self):
        order = {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "contact": self.contact,
            "pickup_location": self.pickup_location,
            "destination": self.destination,
            "weight": self.weight,
            "price": self.price,
            "order_id": self.order_id
        }

        return order
