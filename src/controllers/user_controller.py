from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from main import db, bcrypt
from models import User

user = Blueprint('user', __name__, url_prefix="/user")

#POST endpoints
@user.route("auth", methods=["POST"])
def get_auth():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = data['username']
    password = data['password']

    # find by username
    user = User.query.filter_by(username=username).first()

    # If user doesn't exist of password incorrect
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify ({"error": "Invalid username or password"}), 401
    
    # Create token
    access_token = create_access_token(identity=user.id)
    return jsonify ({"access token": access_token})