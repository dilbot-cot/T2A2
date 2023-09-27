from flask import Blueprint, jsonify, request
from main import db
from models import Movie, User
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
    db.session.add(new_movie)
    db.session.commit()

    return jsonify (movie_schema.dump(new_movie))