from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from main import db, bcrypt
from models import User, Review
from schemas import reviews_schema
from sqlalchemy.orm import joinedload
from .utils import get_current_user

user = Blueprint('user', __name__, url_prefix="/user")

# GET method
@user.route("reviews", methods=["GET"]) # Gets all reviews posted by current user
@jwt_required()
def list_reviews():
    # Authenticate user
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    # gets all reviews including the movie or tv show details
    reviews = Review.query.options(
        joinedload(Review.movie),
        joinedload(Review.tv_show)
        ).filter_by(user_id=current_user.id).all()
    return jsonify (reviews_schema.dump(reviews))

# POST methods
@user.route("auth", methods=["POST"]) # login route - outputs the bearer token
def get_auth():
    data = request.get_json()
    # checks JSON contains username and password
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = data['username']
    password = data['password']
    # Searches for user in database 
    user = User.query.filter_by(username=username).first()
    # If incorrect password/username combo, return error
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify ({"error": "Invalid username or password"}), 401
    # output the token
    access_token = create_access_token(identity=user.id)
    return jsonify ({"access token": access_token})

@user.route("reg", methods=["POST"]) # new user
def new_user():
    # Make sure JSON has data required
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing username, email or password"}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    exisiting_user = User.query.filter_by(username=username).first()
    exisiting_email = User.query.filter_by(email=email).first()
    # Checks if username or email has been used previously
    if exisiting_user or exisiting_email:
        return jsonify({"error": "Username or email already exists"}), 409
    # Creates new user and hashes password
    new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"User {username} created successfully"}), 201

# DELETE method
@user.route("/", methods=["DELETE"])
@jwt_required()
def delete_user():
    # Login user
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    # try to delete user, raise exception if error occurs
    try:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({"message": f"User '{current_user.username}' successfully deleted"}), 200
    except Exception:
        return jsonify({"error": "An error occured while attempting to delete the user"}), 500