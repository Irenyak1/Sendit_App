from flask import Flask, request, jsonify, make_response


app = Flask(__name__)


@app.route('/')
def index():
    """ Endpoint to get the index page of the application"""
    my_response = "You are most welcome to our home page"
    return jsonify(my_response), 200
