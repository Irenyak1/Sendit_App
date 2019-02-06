
users_list = []
""" This is a list that will store all the users """


class User:
    """
    This is the user class which defines the user in terms of
    the user_name, password and role.
    """

    def __init__(self, user_name, email, password, role):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "user_id": len(users_list)+1,
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }

orders_list = []
""" This is a list that will store all the selivery orders made """


class Order:
    """
    This class defines a parcel delivery order in terms of
    user_id, user_name, contact, pickup_location,
    destination, weight, price and status,
    """

    def __init__(self, user_id, user_name, contact, pickup_location,
                 destination, weight, price, status):
        self.user_id = user_id
        self.user_name = user_name
        self.contact = contact
        self.pickup_location = pickup_location
        self.destination = destination
        self.weight = weight
        self.price = price
        self.status = status

    def to_dict(self):
        return {
            "order_id": len(orders_list) + 1,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "contact": self.contact,
            "pickup_location": self.pickup_location,
            "destination": self.destination,
            "weight": self.weight,
            "price": self.price,
            "status": self.status
        }
