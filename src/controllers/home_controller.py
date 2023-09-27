from flask import Blueprint, jsonify


home = Blueprint('home', __name__, url_prefix="/")

@home.route("/", methods=["GET"])
def hello_world():
    return jsonify ({
        "Actions": "You can select from the following endpoints",
        "Register": "You can create yourself as a user by naviagting to '/user/reg' and inputting a 'username', 'email' and 'password'",
        "Login": "naviagte to '/user/auth' to login and obtain your token",
        "Delete User": "navigate to 'user' and ensure you have passed your authentication token, you can then delete yourself as a user"
        })