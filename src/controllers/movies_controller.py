from flask import Blueprint, jsonify, request
from models import Movie, Actor, Director, Genre
from schemas import movie_schema, movies_list_schema
from flask_jwt_extended import jwt_required
from .utils import get_or_404, validate_json_fields, parse_date, append_relation_to_resource, commit_and_respond, get_current_user
from main import db

movies = Blueprint('movies', __name__, url_prefix="/movies")

@movies.route("/", methods=["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_list_schema.dump(all_movies)
    return jsonify(result)

@movies.route("<int:id>", methods=["GET"])
def get_movie(id):
    movie = get_or_404(Movie, id)
    result = movie_schema.dump(movie)
    return jsonify(result)

@movies.route("/", methods=["POST"])
@jwt_required()
def new_movie():
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    required_fields = ['title', 'release_date']
    data, error_response, status_code = validate_json_fields(required_fields)
    if error_response:
        return error_response, status_code
    existing_movie = Movie.query.filter_by(title=data['title']).first()
    if existing_movie:
        return jsonify({"error": "Movie already exists in database"}), 400
    title = data['title']
    release_date_str = data['release_date']
    release_date, error_response, status_code = parse_date(release_date_str)
    if error_response:
        return error_response, status_code

    new_movie = Movie(title=title, release_date=release_date)
    db.session.add(new_movie)

    for relation_type in ['actor', 'director', 'genre']:
        relation_id = data.get(f'{relation_type}.id', None)
        if relation_id:
            relation = db.session.query(eval(relation_type.capitalize())).get(relation_id)
            if relation:
                append_relation_to_resource(new_movie, relation, lambda resource, r: getattr(resource, f"{relation_type}s").append(r))
            else:
                return jsonify({"error": f"{relation_type.capitalize()} not found"}), 404

    return commit_and_respond(new_movie, movie_schema)

@movies.route("/<int:id>/actor", methods=["PUT"])
@jwt_required()
def add_actor_to_movie(id):
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    movie = get_or_404(Movie, id)
    data = request.get_json()
    actor_id = data.get('actor.id', None)
    if not actor_id:
        return jsonify({"error": "Missing actor.id"}), 400
    actor = get_or_404(Actor, actor_id)
    append_relation_to_resource(movie, actor, lambda resource, relation: resource.actors.append(relation))
    return commit_and_respond(movie, movie_schema)

@movies.route("/<int:id>/director", methods=["PUT"])
@jwt_required()
def add_director_to_movie(id):
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    movie = get_or_404(Movie, id)
    data = request.get_json()
    director_id = data.get('director.id', None)
    if not director_id:
        return jsonify({"error": "Missing director.id"}), 400
    director = get_or_404(Director, director_id)
    append_relation_to_resource(movie, director, lambda resource, relation: resource.directors.append(relation))
    return commit_and_respond(movie, movie_schema)

@movies.route("/<int:id>/genre", methods=["PUT"])
@jwt_required()
def add_genre_to_movie(id):
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    movie = get_or_404(Movie, id)
    data = request.get_json()
    genre_id = data.get('genre.id', None)
    if not genre_id:
        return jsonify({"error": "Missing genre.id"}), 400
    genre = get_or_404(Genre, genre_id)
    append_relation_to_resource(movie, genre, lambda resource, relation: resource.genres.append(relation))
    return commit_and_respond(movie, movie_schema)

@movies.route("/<int:id>/end_date", methods=["PUT"])
@jwt_required()
def add_end_date_to_movie(id):
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    movie = get_or_404(Movie, id)
    data = request.get_json()
    end_date_str = data.get('end_date', None)
    if not end_date_str:
        return jsonify ({"error": "Missing end_date"}), 400
    end_date, error_response, status_code = parse_date(end_date_str)
    if error_response:
        return error_response, status_code
    movie.end_date = end_date
    return commit_and_respond(movie, movie_schema)