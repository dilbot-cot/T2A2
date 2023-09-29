from flask import Blueprint, jsonify, request
from models import Movie, Actor, Director, Genre
from schemas import movie_schema, movies_list_schema
from flask_jwt_extended import jwt_required
from .utils import get_or_404, validate_json_fields, parse_date, append_relation_to_resource, commit_and_respond, get_current_user
from main import db

movies = Blueprint('movies', __name__, url_prefix="/movies")

# GET methods
@movies.route("/", methods=["GET"])
# Get list of all movies
def get_movies():
    all_movies = Movie.query.all()
    result = movies_list_schema.dump(all_movies)
    return jsonify(result)

@movies.route("<int:id>", methods=["GET"])
# Get list of specific movie with all details
def get_movie(id):
    movie = get_or_404(Movie, id)
    result = movie_schema.dump(movie)
    return jsonify(result)

# POST method
@movies.route("/", methods=["POST"])
@jwt_required()
# Creates new movie
def new_movie():
    # Authenticates that the user is logged in
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # fetch JSON
    data, error_response, status_code = validate_json_fields(['title', 'release_date'])
    if error_response:
        return error_response, status_code
    # seach if the movie already exists
    existing_movie = Movie.query.filter_by(title=data['title']).first()
    if existing_movie:
        return jsonify({"error": "Movie already exists in database"}), 400
    # parse the date to ensure it is in the correct format
    release_date_str = data['release_date']
    release_date, error_response, status_code = parse_date(release_date_str)
    if error_response:
        return error_response, status_code

    new_movie = Movie(title=data['title'], release_date=release_date) # Mandatory fields to create the movie
    db.session.add(new_movie) # add the movie to db (not yet commited)

    # Loop through possible optional fields and append if they exist
    for relation_type in ['actor', 'director', 'genre']:
        relation_id = data.get(f'{relation_type}.id', None)
        if relation_id:
            relation = db.session.query(eval(relation_type.capitalize())).get(relation_id)
            if relation:
                append_relation_to_resource(new_movie, relation, lambda resource, r: getattr(resource, f"{relation_type}s").append(r))
            else:
                return jsonify({"error": f"{relation_type.capitalize()} not found"}), 404

    return commit_and_respond(new_movie, movie_schema)

# PUT methods
@movies.route("/<int:id>/actor", methods=["PUT"])
@jwt_required()
def add_actor_to_movie(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Checks that movie exists in db
    movie = get_or_404(Movie, id)
    data = request.get_json()
    actor_id = data.get('actor.id', None)
    # Make sure JSON contains required field
    if not actor_id:
        return jsonify({"error": "Missing actor.id"}), 400
    # Checks if the actor exists in database
    actor = get_or_404(Actor, actor_id)
    append_relation_to_resource(movie, actor, lambda resource, relation: resource.actors.append(relation))
    return commit_and_respond(movie, movie_schema)

@movies.route("/<int:id>/director", methods=["PUT"])
@jwt_required()
def add_director_to_movie(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Checks that movie exists in db
    movie = get_or_404(Movie, id)
    data = request.get_json()
    director_id = data.get('director.id', None)
    # Make sure JSON contains required field
    if not director_id:
        return jsonify({"error": "Missing director.id"}), 400
    # Checks if the director exists in database
    director = get_or_404(Director, director_id)
    append_relation_to_resource(movie, director, lambda resource, relation: resource.directors.append(relation))
    return commit_and_respond(movie, movie_schema)

@movies.route("/<int:id>/genre", methods=["PUT"])
@jwt_required()
def add_genre_to_movie(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Checks that movie exists in db
    movie = get_or_404(Movie, id)
    data = request.get_json()
    genre_id = data.get('genre.id', None)
    # Make sure JSON contains required field
    if not genre_id:
        return jsonify({"error": "Missing genre.id"}), 400
    # Checks if the genre exists in database
    genre = get_or_404(Genre, genre_id)
    append_relation_to_resource(movie, genre, lambda resource, relation: resource.genres.append(relation))
    return commit_and_respond(movie, movie_schema)