from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models import User
from schemas import users_list_schema

admin = Blueprint('admin', __name__, url_prefix="/admin")

#GET endpoints
@admin.route("/", methods=["GET"])
@jwt_required()
def get_users():
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # if passed, provide the list of users
    all_users = User.query.all()
    result = users_list_schema.dump(all_users)
    return jsonify(result)