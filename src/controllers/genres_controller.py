from flask import Blueprint, jsonify
from main import db
from models import Genre, User
from schemas import genre_schema, genres_list_schema
from flask_jwt_extended import jwt_required
from .utils import get_or_404, validate_json_fields, commit_and_respond, get_current_user

genres = Blueprint('genres', __name__, url_prefix="/genres")

# GET methods
@genres.route("/", methods=["GET"])
# List all genres
def get_genres():
    all_genres = Genre.query.all()
    result = genres_list_schema.dump(all_genres)
    return jsonify(result)

@genres.route("<int:id>", methods=["GET"])
# List specific genre and details
def get_genre(id):
    genre = get_or_404(Genre, id)
    result = genre_schema.dump(genre)
    return jsonify(result)

# POST methods
@genres.route("/", methods=["POST"])
@jwt_required()
# Creates new genre
def new_genre():
    # make sure user is logged in
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # fetch JSON data
    data, error, status_code = validate_json_fields(['name'])
    if error:
        return error, status_code
    # Check if the genre already exists
    existing_genre = Genre.query.filter_by(name=data['name']).first()
    if existing_genre:
        return jsonify({"error": "Genre already exists in database"}), 400
    # Add the genre
    new_genre = Genre(name=data['name'])
    db.session.add(new_genre)
    return commit_and_respond(new_genre, genre_schema)