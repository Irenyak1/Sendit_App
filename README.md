# sendit_app
[![Build Status](https://www.travis-ci.com/Irenyak1/sendit-app.svg?branch=challenge_2)](https://www.travis-ci.com/Irenyak1/sendit-app)
[![Maintainability](https://api.codeclimate.com/v1/badges/c4b899b926f66724b028/maintainability)](https://codeclimate.com/github/Irenyak1/sendit-app/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Irenyak1/sendit-app/badge.svg?branch=ft-%23161808742-create-order)](https://coveralls.io/github/Irenyak1/sendit-app?branch=ft-%23161808742-create-order)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f5c1014e426d4a30b5e8e1bd0d5c3a19)](https://www.codacy.com/app/Irenyak1/sendit-app?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Irenyak1/sendit-app&amp;utm_campaign=Badge_Grade)



## Description
Sendit_App is an application that enables people to send and recieve parcels to and from different places across the globe. This App  allows the admin to monitor Parcel orders from different users. The admin can be able to know the parcels being sent, their pickup and drop off locations. It also enables the user to create an account and login and then send his or her parcel to any destination of the world. The user can also be able see the number of orders 
they have made. 

## Getting Started
Follow the following steps to get a copy of the API to run on your machine.

### Prerequisites

Install the following programs before using the API:
```
1. Python version 3.6.7
2. Postman
3. Any IDE of your choice e.g Vscode, SublimeText, etc
```

## Instructions for set up
- Clone this repo using:
```
git clone https://github.com/Irenyak1/sendit-app/tree/challenge_2
```
### Set up a virtual environment for python in the project directory
To set up the virtual environment, you need to install virtualenv which is a python package using pip.
Run the command below to install it.
- `pip install virtualenv` installs virtualenv.
- `virtualenv venv`  to create a virtual environment called venv.
- `source venv/bin/activate` to activate your virtual environment on ubuntu.
- `deactivate` to deactivate your virtual environment on ubuntu.
- `venv/Scripts/activate` to activate your virtual environment on windows.
- `venv/Scripts/deactivate` to deactivate your virtual environment on windows.

### Install the required packages using
After you have set up and activated virtual environment, it's time now to install all the packages that the project requires.
```
pip install -r requirements.txt
```

### Running the application
Use the following command in the project folder to run the app:
```
python run.py
```
### Running the tests

Use the following command to run the tests in your virtual environment:
```
pytest 
pytest --cov to see coverage
```
## Authentication API ENDPOINTS
|HTTP method|  End point        |Functionality        | 
|-----------|-------------------|---------------------|
|POST       |/api/v1/auth/signup|Signup a new user    |
|POST       |/api/v1/auth/login |Login a user or admin|


## sendit_app API ENDPOINTS

| HTTP method|    End point                    | Functionality                     |
| -----------| ------------------------------- | --------------------------------- |
| GET        | /api/v1/                        | A welcome route to the application|
| GET        | /api/v1/users                   | Fetches all signed up users       |
| GET        | /api/v1/users/<int:user_id>     | Fetches a single user             |
| POST       | /api/v1/orders                  | Creates a delivery order          |
| GET        | /api/v1/orders                  | Fetches all delivery orders       |
| GET        | /api/v1/orders/<int:order_id>   | Fetches a single delivery order   |
| GET        | /api/v1/users/<int:user_id>/orders| Fetches all orders by a given user|
| GET | /api/v1/orders/users/<int:order_id>/<int:user_id>| Fetches a single order by a given user|
| PUT        | /api/v1/orders/<int:order_id>/cancel| Cancels an order              |
| PUT | /api/v1/orders/users/<int:order_id>/<int:user_id>/cancel| Cancels an order by a given user| 
| PUT  | /api/v1/orders/users/<int:user_id>/cancel_all| Cancels all orders by a given user         
| PUT        | /api/v1/orders/cancel            | Cancels all orders made|


#### Sample Data you can use to test in postman
```
User signup.
{
	"user_name":"irenyak",
	"email": "gigalasl@gmail.com",
	"password": "gigals",
	"role": "user"
}

User Login.
{
	"username": "irenyak",
	"password": "gigals"
}

Creating a delivery order
{
	"user_id":1,
  "user_name" : "irenyak",
  "contact" :12345678,
  "pickup_location" :"City square",
  "destination" :"Gayaza",
  "weight": 10,
  "price":20000,
  "status":"pending"
}

``` 

#### Sample output after user signup
```
{
    "message": "Thank you for signing up",
    "new_user": {
        "email": "gigalasl@gmail.com",
        "password": "gigals",
        "role": "user",
        "user_id": 1,
        "user_name": "irenyak"
    },
    "status": 201
}
```

#### Sample output after user login
```
{
    "message": "You have successfully logged in",
    "status": 200,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX25hbWUiOiJpcmVueWFrIiwiZXhwIjoxNTUyMzc1MTQ3fQ.cV0Z85OYUE4CvJMpE34Eeyfau2R-pwXeQZq3yXYl1WA",
    "user": {
        "email": "gigalasl@gmail.com",
        "password": "gigals",
        "role": "user",
        "user_id": 1,
        "user_name": "irenyak"
    }
}
```
#### Adding Token to headers using Postman
- While in Postman, select an API method.
- Click the Authorization tab.
- Choose Bearer Token.
- Copy the token above and paste it in the edit text box provided on the right hand side.

### Technologies used to build the application
 - [Python 3.6](https://docs.python.org/3/)- Programming language
 - [Flask](http://flask.pocoo.org/) - Micro web framework for Python
 - [PIP](https://pip.pypa.io/en/stable/) - A python package installer


## Tools Used
- Pivotal Tracker used to write user stories for this project
- Visual Studio Code as the editor for the project files 
- Github
- Postman used to test the api end points

## Deployment
- The link to ***Heroku*** where the api is deployed [here](https://irynexsendit.herokuapp.com/).
- To access other routes append the api end points stated above to the home route.

### Authors
Irene Nyakate

