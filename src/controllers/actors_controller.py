from flask import Blueprint, jsonify, request
from main import db
from models import Actor, User
from schemas import actors_list_schema, actor_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

actors = Blueprint('actors', __name__, url_prefix="/actors")

#GET endpoints
@actors.route("/", methods=["GET"])
def get_actors():
    # route gets all the actors without delving into the nested fields
    # this will be handled when looking at the specific actor
    all_actors = Actor.query.all()
    result = actors_list_schema.dump(all_actors)
    return jsonify(result)

@actors.route("<int:id>", methods=["GET"])
def get_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        return jsonify ({"error": "Actor not found"}), 404
    result = actor_schema.dump(actor)
    return jsonify (result)

#POST endpoints
# New Actor
@actors.route("/", methods=["POST"])
@jwt_required()
def new_actor():
    # First check that the user exists in DB
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify ({"error": "You are not authorised to perform this action, please login first"}), 401
    
    data  = request.get_json()
    if not data or 'name' not in data or 'dob' not in data:
        return jsonify({"error": "Missing actor details"}), 400
    
    name = data['name']
    dob_str = data['dob']

    try:
        dob = datetime.strptime(dob_str, '%d/%m/%Y').date()
    except ValueError:
        return jsonify ({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400

    # find by name if the actor alread exists
    existing_actor = Actor.query.filter_by(name=name).first()

    # If actor already exists, return error
    if existing_actor:
        return jsonify ({"error": "Actor already exists in database"}), 400
    
    # create new actor
    new_actor = Actor(name=name, dob=dob)
    db.session.add(new_actor)
    db.session.commit()

    return jsonify (actor_schema.dump(new_actor))