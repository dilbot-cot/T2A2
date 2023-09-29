from flask import Blueprint, jsonify, request
from models import TVShow, Actor, Director, Genre
from schemas import tvshow_schema, tvshows_list_schema
from flask_jwt_extended import jwt_required
from .utils import get_or_404, validate_json_fields, parse_date, append_relation_to_resource, commit_and_respond, get_current_user
from main import db

tv_shows = Blueprint('tv_shows', __name__, url_prefix="/tv_shows")

# GET methods
@tv_shows.route("/", methods=["GET"])
# get list of all tv shows
def get_tv_shows():
    all_tv_shows = TVShow.query.all()
    result = tvshows_list_schema.dump(all_tv_shows)
    return jsonify(result)

@tv_shows.route("<int:id>", methods=["GET"])
# get list of specific tv show with all details
def get_tv_show(id):
    tv_show = get_or_404(TVShow, id)
    result = tvshow_schema.dump(tv_show)
    return jsonify(result)

# POST method
@tv_shows.route("/", methods=["POST"])
@jwt_required()
# creates new tv show
def new_tv_show():
    # Checks user is logged in
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # get JSON details
    data, error_response, status_code = validate_json_fields(['title', 'start_date'])
    if error_response:
        return error_response, status_code
    # see if tv show alread exists in database
    existing_tv_show = TVShow.query.filter_by(title=data['title']).first()
    if existing_tv_show:
        return jsonify({"error": "TV Show already exists in database"}), 400
    # check that the start date is in correct format
    start_date_str = data['start_date']
    start_date, error_response, status_code = parse_date(start_date_str)
    if error_response:
        return error_response, status_code
    # check that the end date is in the correct format or is blank
    end_date_str = data.get('end_date', None)
    if end_date_str:
        end_date, error_response, status_code = parse_date(end_date_str)
        if error_response:
            return error_response, status_code
    else:
        end_date = None

    new_tv_show = TVShow(title=data['title'], start_date=start_date, end_date=end_date) # Adds all fields
    db.session.add(new_tv_show) # add the tv show to database

    # Loop through possible fields and append if they exist
    for relation_type in ['actor', 'director', 'genre']:
        relation_id = data.get(f'{relation_type}.id', None)
        if relation_id:
            relation = db.session.query(eval(relation_type.capitalize())).get(relation_id)
            if relation:
                append_relation_to_resource(new_tv_show, relation, lambda resource, r: getattr(resource, f"{relation_type}s").append(r))
            else:
                return jsonify({"error": f"{relation_type.capitalize()} not found"}), 404

    return commit_and_respond(new_tv_show, tvshow_schema)

# PUT methods
@tv_shows.route("/<int:id>/actor", methods=["PUT"])
@jwt_required()
def add_actor_to_tv_show(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Checks that TV Show exists in db
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    actor_id = data.get('actor.id', None)
    # Make sure JSON contains required field
    if not actor_id:
        return jsonify({"error": "Missing actor.id"}), 400
    # Checks if the actor exists in database
    actor = get_or_404(Actor, actor_id)
    append_relation_to_resource(tv_show, actor, lambda resource, relation: resource.actors.append(relation))
    return commit_and_respond(tv_show, tvshow_schema)

@tv_shows.route("/<int:id>/director", methods=["PUT"])
@jwt_required()
def add_director_to_tv_show(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Checks that TV Show exists in db
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    director_id = data.get('director.id', None)
    # Make sure JSON contains required field
    if not director_id:
        return jsonify({"error": "Missing director.id"}), 400
    # Checks if the director exists in database
    director = get_or_404(Director, director_id)
    append_relation_to_resource(tv_show, director, lambda resource, relation: resource.directors.append(relation))
    return commit_and_respond(tv_show, tvshow_schema)

@tv_shows.route("/<int:id>/genre", methods=["PUT"])
@jwt_required()
def add_genre_to_tv_show(id):
    # Authenticate user
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    # Checks that TV Show exists in db
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    genre_id = data.get('genre.id', None)
    # Make sure JSON contains required field
    if not genre_id:
        return jsonify({"error": "Missing genre.id"}), 400
     # Checks if the genre exists in database
    genre = get_or_404(Genre, genre_id)
    append_relation_to_resource(tv_show, genre, lambda resource, relation: resource.genres.append(relation))
    return commit_and_respond(tv_show, tvshow_schema)

@tv_shows.route("/<int:id>/end_date", methods=["PUT"])
@jwt_required()
def add_end_date_to_tv_show(id):
    _, error, status_code = get_current_user()
    if error:
        return error, status_code
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    end_date_str = data.get('end_date', None)
    # Make sure JSON contains required field
    if not end_date_str:
        return jsonify ({"error": "Missing end_date"}), 400
    # check end_date matches correct format
    end_date, error_response, status_code = parse_date(end_date_str)
    if error_response:
        return error_response, status_code
    
    tv_show.end_date = end_date
    return commit_and_respond(tv_show, tvshow_schema)