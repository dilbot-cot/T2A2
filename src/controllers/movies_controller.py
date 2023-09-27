from flask import Blueprint, jsonify, request
from main import db
from models import Movie, User, Actor, Director, Genre
from schemas import movie_schema, movies_list_schema, movies_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

movies = Blueprint('movies', __name__, url_prefix="/movies")

#GET endpoints
@movies.route("/", methods=["GET"])
def get_movies():
    # route gets all the movies without delving into the nested fields
    # this will be handled when looking at the specific movie
    all_movies = Movie.query.all()
    result = movies_list_schema.dump(all_movies)
    return jsonify(result)

@movies.route("<int:id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify ({"error": "Movie not found"}), 404
    result = movie_schema.dump(movie)
    return jsonify (result)

#POST endpoints
# New movie
@movies.route("/", methods=["POST"])
@jwt_required()
def new_movie():
    # First check that the user exists in DB
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify ({"error": "You are not authorised to perform this action, please login first"}), 401
    
    data  = request.get_json()
    if not data or 'title' not in data or 'release_date' not in data:
        return jsonify({"error": "Missing movie details"}), 400
    
    title = data['title']
    release_date_str = data['release_date']
    actor_id = data.get('actor.id', None)
    director_id = data.get('director.id', None)
    genre_id = data.get('genre.id', None)

    try:
        release_date = datetime.strptime(release_date_str, '%d/%m/%Y').date()
    except ValueError:
        return jsonify ({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400

    # find by title if the movie alread exists
    existing_movie = Movie.query.filter_by(title=title).first()

    # If movie already exists, return error
    if existing_movie:
        return jsonify ({"error": "Movie already exists in database"}), 400
    
    # create new movie
    new_movie = Movie(title=title, release_date=release_date)

    # if actor details were passed at creation, append
    if actor_id:
        actor = Actor.query.get(actor_id)
        if actor:
            new_movie.actors.append(actor)

    # if director details were passed at creation, append
    if director_id:
        director = Director.query.get(director_id)
        if director:
            new_movie.directors.append(director)

    if genre_id:
        genre = Genre.query.get(genre_id)
        if genre:
            new_movie.genres.append(genre)

    db.session.add(new_movie)
    db.session.commit()

    return jsonify (movie_schema.dump(new_movie))

# PUT endpoints
@movies.route("/<int:id>/actor", methods=["PUT"])
@jwt_required()
def add_actor_to_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify ({"error": "Movie not found"}), 404
    data = request.get_json()
    actor_id = data.get('actor_id', None)

    if not actor_id:
        return jsonify ({"error": "Missing actor_id"}), 400
    
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify ({"error": "Actor not found"}), 404
    
    movie.actors.append(actor)
    db.session.commit()

    return jsonify (movie_schema.dump(movie))

@movies.route("/<int:id>/director", methods=["PUT"])
@jwt_required()
def add_director_to_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify ({"error": "Movie not found"}), 404
    data = request.get_json()
    director_id = data.get('director_id', None)

    if not director_id:
        return jsonify ({"error": "Missing director_id"}), 400
    
    director = Director.query.get(director_id)
    if not director:
        return jsonify ({"error": "Director not found"}), 404
    
    movie.directors.append(director)
    db.session.commit()

    return jsonify (movie_schema.dump(movie))

@movies.route("/<int:id>/genre", methods=["PUT"])
@jwt_required()
def add_genre_to_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify ({"error": "Movie not found"}), 404
    data = request.get_json()
    genre_id = data.get('genre_id', None)

    if not genre_id:
        return jsonify ({"error": "Missing genre_id"}), 400
    
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify ({"error": "Genre not found"}), 404
    
    movie.genres.append(genre)
    db.session.commit()

    return jsonify (movie_schema.dump(movie))