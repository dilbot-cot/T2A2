from flask import Blueprint, jsonify, request
from main import db
from models import Director, User
from schemas import directors_list_schema, director_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

directors = Blueprint('directors', __name__, url_prefix="/directors")

#GET endpoints
@directors.route("/", methods=["GET"])
def get_directors():
    # route gets all the directors without delving into the nested fields
    # this will be handled when looking at the specific director
    all_directors = Director.query.all()
    result = directors_list_schema.dump(all_directors)
    return jsonify(result)

@directors.route("<int:id>", methods=["GET"])
def get_director(id):
    director = Director.query.get(id)
    if not director:
        return jsonify ({"error": "Director not found"}), 404
    result = director_schema.dump(director)
    return jsonify (result)

#POST endpoints
# New Director
@directors.route("/", methods=["POST"])
@jwt_required()
def new_director():
    # First check that the user exists in DB
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify ({"error": "You are not authorised to perform this action, please login first"}), 401
    
    data  = request.get_json()
    if not data or 'name' not in data or 'dob' not in data:
        return jsonify({"error": "Missing director details"}), 400
    
    name = data['name']
    dob_str = data['dob']

    try:
        dob = datetime.strptime(dob_str, '%d/%m/%Y').date()
    except ValueError:
        return jsonify ({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400

    # find by name if the director alread exists
    existing_director = Director.query.filter_by(name=name).first()

    # If director already exists, return error
    if existing_director:
        return jsonify ({"error": "Director already exists in database"}), 400
    
    # create new director
    new_director = Director(name=name, dob=dob)
    db.session.add(new_director)
    db.session.commit()

    return jsonify (director_schema.dump(new_director))