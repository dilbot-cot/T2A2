from flask import Blueprint, jsonify, request
from main import db
from models import Actor, Movie, TVShow
from schemas import actors_list_schema, actor_schema
from flask_jwt_extended import jwt_required
from .utils import get_or_404, validate_json_fields, parse_date, append_relation_to_resource, commit_and_respond, get_current_user

actors = Blueprint('actors', __name__, url_prefix="/actors")

# GET methods
@actors.route("/", methods=["GET"])
# Gets a list of all actors, with limited info passed from actors_list_schema
def get_actors(): 
    all_actors = Actor.query.all()
    result = actors_list_schema.dump(all_actors)
    return jsonify(result)

@actors.route("<int:id>", methods=["GET"])
# Gets all info from a specific actor based on id
def get_actor(id):
    actor = get_or_404(Actor, id)
    result = actor_schema.dump(actor)
    return jsonify (result)

# POST method
@actors.route("/", methods=["POST"])
@jwt_required()
# Creates a new actor 
def new_actor():
    # authenticate the user calling the get_current_user function from utils.py
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # fetch the data from JSON payload
    data, error, status_code = validate_json_fields(['name', 'dob'])
    if error:
        return error, status_code
    # parse the dob string through the parse_date funtion from utils.py
    dob, error, status_code = parse_date(data['dob'])
    if error:
        return error, status_code
    # search if the actor name appears in the database already
    existing_actor = Actor.query.filter_by(name=data['name']).first()
    if existing_actor:
        return jsonify({"error": "Actor already exists in database"}), 400
    
    new_actor = Actor(name=data['name'], dob=dob) # Mandatory fields to create the actor
    db.session.add(new_actor) # Adds the actor as we have all mandatory fields

    # optional fields are then iterated
    for relation_type in ['movie', 'tv_show']:
        class_name = 'Movie' if relation_type == 'movie' else 'TVShow'
        relation_id = data.get(f'{relation_type}.id', None)
        if relation_id: # if movie.id ot tv_show.id has value
            relation = db.session.query(eval(class_name)).get(relation_id)
            # If the details listed for the ids is valid, append it to the new_actor, else error
            if relation:
                append_relation_to_resource(new_actor, relation, lambda resource, r: getattr(resource, f"{relation_type}s").append(r))
            else:
                return jsonify ({"error": f"{relation_type.capitalize()} not found"}), 404
    
    return commit_and_respond(new_actor, actor_schema)

# PUT Methods
@actors.route("/<int:id>/tv", methods=["PUT"])
@jwt_required()
def add_tv_show_to_actor(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Check if actor exists in database
    actor = get_or_404(Actor, id)
    data = request.get_json()
    tv_show_id = data.get('tv_show.id', None)
    # Make sure json payload includes required field
    if not tv_show_id:
        return jsonify ({"error": "Missing tv_show_id"}), 400
    # Check if the tv_show being linked exists in database
    tv_show = get_or_404(TVShow, tv_show_id)
    append_relation_to_resource(actor, tv_show, lambda resource, relation: resource.tv_shows.append(relation))
    return commit_and_respond(actor, actor_schema)

@actors.route("/<int:id>/movie", methods=["PUT"])
@jwt_required()
def add_movie_to_actor(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Check if actor exists in database
    actor = get_or_404(Actor, id)
    data = request.get_json()
    movie_id = data.get('movie.id', None)
    # Make sure json payload includes required field
    if not movie_id:
        return jsonify ({"error": "Missing movie.id"}), 400
    # Check if the movie being linked exists in database
    movie = get_or_404(Movie, movie_id)
    append_relation_to_resource(actor, movie, lambda resource, relation: resource.movies.append(relation))
    return commit_and_respond(actor, actor_schema)