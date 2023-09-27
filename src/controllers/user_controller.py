from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from main import db, bcrypt
from models import User

user = Blueprint('user', __name__, url_prefix="/user")

#POST endpoints
# Get authentication token
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

# Create a new user
@user.route("reg", methods=["POST"])
def new_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing username, email or password"}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']

    # find username and email
    exisiting_user = User.query.filter_by(username=username).first()
    exisiting_email = User.query.filter_by(email=email).first()

    if exisiting_user or exisiting_email:
        return jsonify({"error": "Username or email already exists"}), 409
    
    # Create new user
    new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))

    # Add user to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {username} created successfully"}), 201


#DELETE endpoints
@user.route("/", methods=["DELETE"])
@jwt_required()
def delete_user():
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not authorised to perform this action"}), 401
    
    try:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({"message": f"User '{current_user.username}' successfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": "An error occured while attempting to delete the user"}), 500