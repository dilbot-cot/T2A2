from flask import Blueprint, jsonify, request
from main import db
from models import Director, User, Movie, TVShow
from schemas import directors_list_schema, director_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from .utils import get_or_404

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
    director = get_or_404(Director, id)
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
    movie_id = data.get('movie.id', None)
    tv_show_id = data.get('tv_show.id', None)

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

        # if movie details were passed at creation, append
    if movie_id:
        movie = Movie.query.get(movie_id)
        if movie:
            new_director.movies.append(movie)

    # if tv_show details were passed at creation, append
    if tv_show_id:
        tv_show = TVShow.query.get(tv_show_id)
        if tv_show:
            new_director.tv_shows.append(tv_show)

    db.session.add(new_director)
    db.session.commit()

    return jsonify (director_schema.dump(new_director))

@directors.route("/<int:id>/movie", methods=["PUT"])
@jwt_required()
def add_movie_to_director(id):
    director = get_or_404(Director, id)
    data = request.get_json()
    movie_id = data.get('movie_id', None)

    if not movie_id:
        return jsonify ({"error": "Missing movie_id"}), 400
    
    movie = get_or_404(Movie, movie_id)
    
    director.movies.append(movie)
    db.session.commit()

    return jsonify (director_schema.dump(director))


@directors.route("/<int:id>/tv", methods=["PUT"])
@jwt_required()
def add_tv_show_to_director(id):
    director = get_or_404(Director, id)
    data = request.get_json()
    tv_show_id = data.get('tv_show_id', None)

    if not tv_show_id:
        return jsonify ({"error": "Missing tv_show_id"}), 400
    
    tv_show = get_or_404(TVShow, tv_show_id)
    
    director.tv_shows.append(tv_show)
    db.session.commit()

    return jsonify (director_schema.dump(director))