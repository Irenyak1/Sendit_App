# Sendit_App
[![Build Status](https://www.travis-ci.com/Irenyak1/Sendit_App.svg?branch=challenge_2)](https://www.travis-ci.com/Irenyak1/Sendit_App)
[![Maintainability](https://api.codeclimate.com/v1/badges/13ad5e9cefc8a9737d98/maintainability)](https://codeclimate.com/github/Irenyak1/Sendit_App/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Irenyak1/Sendit_App/badge.svg?branch=ft-%23161808742-create-order)](https://coveralls.io/github/Irenyak1/Sendit_App?branch=ft-%23161808742-create-order)


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



  ### Authors
Irene Nyakate

