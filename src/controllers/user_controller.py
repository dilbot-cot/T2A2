from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from main import db, bcrypt
from models import User, Review
from schemas import reviews_schema
from sqlalchemy.orm import joinedload
from .utils import get_current_user

user = Blueprint('user', __name__, url_prefix="/user")

@user.route("reviews", methods=["GET"])
@jwt_required()
def list_reviews():
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    reviews = Review.query.options(
        joinedload(Review.movie),
        joinedload(Review.tv_show)
        ).filter_by(user_id=current_user.id).all()
    return jsonify (reviews_schema.dump(reviews))

@user.route("auth", methods=["POST"])
def get_auth():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify ({"error": "Invalid username or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify ({"access token": access_token})

@user.route("reg", methods=["POST"])
def new_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing username, email or password"}), 400
    username = data['username']
    email = data['email']
    password = data['password']
    exisiting_user = User.query.filter_by(username=username).first()
    exisiting_email = User.query.filter_by(email=email).first()
    if exisiting_user or exisiting_email:
        return jsonify({"error": "Username or email already exists"}), 409
    new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"User {username} created successfully"}), 201

@user.route("/", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    try:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({"message": f"User '{current_user.username}' successfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": "An error occured while attempting to delete the user"}), 500