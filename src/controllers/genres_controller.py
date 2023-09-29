from flask import Blueprint, jsonify, request
from main import db
from models import Genre, User
from schemas import genre_schema, genres_list_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import get_or_404

genres = Blueprint('genres', __name__, url_prefix="/genres")

#GET endpoints
@genres.route("/", methods=["GET"])
def get_genres():
    # route gets all the genres without delving into the nested fields
    # this will be handled when looking at the specific genre
    all_genres = Genre.query.all()
    result = genres_list_schema.dump(all_genres)
    return jsonify(result)

@genres.route("<int:id>", methods=["GET"])
def get_genre(id):
    genre = get_or_404(Genre, id)
    result = genre_schema.dump(genre)
    return jsonify (result)

#POST endpoints
# New Genre
@genres.route("/", methods=["POST"])
@jwt_required()
def new_genre():
    # First check that the user exists in DB
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify ({"error": "You are not authorised to perform this action, please login first"}), 401
    
    data  = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing genre details"}), 400
    
    name = data['name']

    # find by name if the genre alread exists
    existing_genre = Genre.query.filter_by(name=name).first()

    # If genre already exists, return error
    if existing_genre:
        return jsonify ({"error": "Genre already exists in database"}), 400
    
    # create new genre
    new_genre = Genre(name=name)
    db.session.add(new_genre)
    db.session.commit()

    return jsonify (genre_schema.dump(new_genre))