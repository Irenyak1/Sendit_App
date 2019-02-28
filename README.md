# Sendit_App
[![Build Status](https://www.travis-ci.com/Irenyak1/Sendit_App.svg?branch=challenge_2)](https://www.travis-ci.com/Irenyak1/Sendit_App)
[![Maintainability](https://api.codeclimate.com/v1/badges/13ad5e9cefc8a9737d98/maintainability)](https://codeclimate.com/github/Irenyak1/Sendit_App/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/13ad5e9cefc8a9737d98/test_coverage)](https://codeclimate.com/github/Irenyak1/Sendit_App/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/Irenyak1/Sendit_App/badge.svg?branch=ft-%23161808742-create-order)](https://coveralls.io/github/Irenyak1/Sendit_App?branch=ft-%23161808742-create-order)

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
## Description
Sendit_App is an application that enables people to send and recieve parcels to and from different places across the globe. This App  allows the admin to monitor Parcel orders from different users. The admin can be able to know the parcels being sent, their pickup and drop off locations. It also enables the user to create an account and login and then send his or her parcel to any destination of the world. The user can also be able see the number of orders 
they have made. 

## Getting Started
Follow the following steps to get a copy of the API to run on your machine.

### Prerequisites

Install the following programs before using the API:
```
1. Python version 3.5.2
2. Postman
3. Any IDE of your choice
```

## Instructions for set up
- Clone this repo using:
```
git clone https://github.com/Irenyak1/Sendit_App/tree/challenge_2
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

### Install the required packages using:
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

|HTTP method|End point|Functionality| 
|-----------|---------|--------------|
|POST|/api/v1/auth/signup|Register a new user|
|POST|/api/v1/auth/login|Login a user or admin|


## Sendit_App API ENDPOINTS

<!-- # API Endpoints

| REQUEST | ROUTE                           | FUNCTIONALITY                 |
| ------- | ------------------------------- | ----------------------------- |
| GET     | api/v2/products                 | Fetches all products          |
| GET     | api/v2/products/&lt;product_id> | Fetches a single product      |
| PUT     | api/v2/products/&lt;product_id> | Updates a single product      |
| DELETE  | api/v2/products/&lt;product_id> | Deletes a product             |
| GET     | api/v2/sales                    | Fetches all sales records     |
| GET     | api/v2/sales/&lt;sales_id>      | Fetches a single sales record |
| POST    | api/v2/products                 | Creates a product             |
| POST    | api/v2/auth/login               | Logs in a user                |
| POST    | api/v2/auth/signup              | Registers a user              |
| POST    | api/v2/auth/logout              | Logs out a user               |
| POST    | api/v2/sales                    | Creates a sales order          -->
<!-- |HTTP method|End point|Functionality| 
|-----------|---------|--------------|
|POST|/api/v1/red_flags|Create a red-flag record|
|GET|/api/v1/red_flags|Return all red-flags available|
|GET|/api/v1/red_flags/int:red_flag_id|Get a specific red-flag record|
|DELETE|/api/v1/red_flags/int:red_flag_id|Delete specific red-flag record|
|PATCH|/api/v1/red_flags/int:red_flag_id/location|Update location of specific red-flag record| 
|PATCH|/api/v1/red_flags/int:red_flag_id/comment|Update comment of specific red-flag record|
|PATCH|/api/v1/red_flags/int:red_flag_id/status|Admin status of specific red-flag record|


## Intervention API ENDPOINTS

|HTTP method|End point|Functionality| 
|-----------|---------|--------------|
|POST| /api/v1/interventions |Create an intervention record|
|GET| /api/v1/interventions|Get all interventions available|
|GET| /api/v1/interventions/<int:intervention_id> |Get specific intervention record|
|DELETE| /api/v1/interventions/<int:intervention_id>|Delete a specific intervention record|
|PATCH| /api/v1/interventions/<int:intervention_id>/location |Update location of an intervention record|
|PATCH| /api/v1/interventions/<int:intervention_id>/comment |Update comment of an intervention record|
|PATCH| /api/v1/interventions/<int:intervention_id>/status |Admin Update status of an intervention record|


### Other API ENDPOINTS
 |HTTP method|End point|Functionality| 
 |-----------|---------|--------------|
 |GET|/api/v1/|A welcome route to the application|
 |GET|/api/v1/users|Return all registered users| -->
 
 #### Sample Data to use in postman
```
Registering a user.
{
	"firstname": "Mugerwa",
	"lastname": "Fred",
	"othernames": "",
	"email": "rei@gmail.com",
	"phoneNumber": "0757605424",
	"username": "username",
	"password": "Password123",
	"isAdmin": false
}

User Log In.
{
	"username": "username",
	"password": "Password123"
}

Creating a red_flag
{
	"title": "Corruption",
	"comment": "New comment about corruption",
	"images": ["image1","image2"],
	"location": "Lat 11231 Long 14224",
	"videos": ["vid1","vid2"]
}

``` 

#### Sample output after user sign in
```
{
    "data": [
        {
            "id": 1,
            "message": "User login",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImFkbSI6ZmFsc2UsImV4cCI6MTU0ODM1NzMwM30.mAf2rV1a0pA7zaSxnpdnzLz7j9cIxqaT28jbJx5LQrU",
            "user": {
                "email": "rei@gmail.com",
                "firstname": "Mugerwa",
                "id": 1,
                "isadmin": false,
                "lastname": "Fred",
                "othernames": "",
                "password": "sha256$gzLCrEW5$03b8eaf3b101819974be85c9833161f47f1de734779fddb644b2fc626fe6dbce",
                "phonenumber": "0757605424",
                "registered": "Thu, 24 Jan 2019 00:00:00 GMT",
                "username": "username123"
            }
        }
    ],
    "status": 200
}
```
#### Adding Token to headers using Postman
- In Postman, select an API method.
- Click the Authorization tab.
- Choose OAuth 2.0 or Bearer Token.
- Copy the token above and paste it in the edit text box provided on the right hand side.

 ### Built with
 - [Flask](http://flask.pocoo.org/) - Micro web framework for Python
 - [PIP](https://pip.pypa.io/en/stable/) - A python package installer

## Tools Used
- Pivotal Tracker used to write user stories for this project
- Visual Studio acting as an editor for the project files 
- Github
- Postman used to test the api end points

## Deployment
- The link to ***Heroku*** where the api is deployed [here](https://fred-reporter.herokuapp.com/).
- To access other routes append the api end points stated above to the home route.

  ### Authors
Irene Nyakate

