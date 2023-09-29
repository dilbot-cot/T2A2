from flask import Blueprint, jsonify, request
from main import db
from models import Director, Movie, TVShow
from schemas import directors_list_schema, director_schema
from flask_jwt_extended import jwt_required
from .utils import get_or_404, validate_json_fields, parse_date, append_relation_to_resource, commit_and_respond, get_current_user

directors = Blueprint('directors', __name__, url_prefix="/directors")

# GET methods
@directors.route("/", methods=["GET"])
# Gets a list of all directors, with limited info passed from directors_list_schema
def get_directors():
    all_directors = Director.query.all()
    result = directors_list_schema.dump(all_directors)
    return jsonify(result)

@directors.route("<int:id>", methods=["GET"])
# Gets all info from a specific director based on id
def get_director(id):
    director = get_or_404(Director, id)
    result = director_schema.dump(director)
    return jsonify(result)

# POST method
@directors.route("/", methods=["POST"])
@jwt_required()
# Creates a new director
def new_director():
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
    existing_director = Director.query.filter_by(name=data['name']).first()
    if existing_director:
        return jsonify({"error": "Director already exists in database"}), 400
    
    new_director = Director(name=data['name'], dob=dob) # Mandatory fields
    db.session.add(new_director) # Adds the director as all mandatory details have been obtained

# optional fields are then iterated
    for relation_type in ['movie', 'tv_show']:
        class_name = 'Movie' if relation_type == 'movie' else 'TVShow'
        relation_id = data.get(f'{relation_type}.id', None)
        if relation_id: # if movie.id ot tv_show.id has value
            relation = db.session.query(eval(class_name)).get(relation_id)
            # If the details listed for the ids is valid, append it to the new_director, else error
            if relation:
                append_relation_to_resource(new_director, relation, lambda resource, r: getattr(resource, f"{relation_type}s").append(r))
            else:
                return jsonify ({"error": f"{relation_type.capitalize()} not found"}), 404

    return commit_and_respond(new_director, director_schema)

# PUT methods
@directors.route("/<int:id>/tv", methods=["PUT"])
@jwt_required()
def add_tv_show_to_director(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Check if director exists in database
    director = get_or_404(Director, id)
    data = request.get_json()
    tv_show_id = data.get('tv_show.id', None)
    # Make sure json payload includes required field
    if not tv_show_id:
        return jsonify ({"error": "Missing tv_show_id"}), 400
    # Check if the tv_show being linked exists in database
    tv_show = get_or_404(TVShow, tv_show_id)
    append_relation_to_resource(director, tv_show, lambda resource, relation: resource.tv_shows.append(relation))
    return commit_and_respond(director, director_schema)

@directors.route("/<int:id>/movie", methods=["PUT"])
@jwt_required()
def add_movie_to_director(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Check if director exists in database
    director = get_or_404(Director, id)
    data = request.get_json()
    movie_id = data.get('movie.id', None)
    # Make sure json payload includes required field
    if not movie_id:
        return jsonify ({"error": "Missing movie.id"}), 400
    # Check if the movie being linked exists in database
    movie = get_or_404(Movie, movie_id)

    append_relation_to_resource(director, movie, lambda resource, relation: resource.movies.append(relation))
    return commit_and_respond(director, director_schema)