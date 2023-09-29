from flask import Blueprint, jsonify, request
from main import db
from models import TVShow, User, Actor, Director, Genre
from schemas import tvshow_schema, tvshows_list_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from .utils import get_or_404

tv_shows = Blueprint('tv_shows', __name__, url_prefix="/tv_shows")

#GET endpoints
@tv_shows.route("/", methods=["GET"])
def get_tv_shows():
    # route gets all the tv_shows without delving into the nested fields
    # this will be handled when looking at the specific tv_show
    all_tv_shows = TVShow.query.all()
    result = tvshows_list_schema.dump(all_tv_shows)
    return jsonify(result)

@tv_shows.route("<int:id>", methods=["GET"])
def get_tv_show(id):
    tv_show = get_or_404(TVShow, id)
    result = tvshow_schema.dump(tv_show)
    return jsonify (result)

#POST endpoints
# New tv_show
@tv_shows.route("/", methods=["POST"])
@jwt_required()
def new_tv_show():
    # First check that the user exists in DB
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify ({"error": "You are not authorised to perform this action, please login first"}), 401
    
    data  = request.get_json()
    if not data or 'title' not in data or 'start_date' not in data:
        return jsonify({"error": "Missing TV Show details"}), 400
    
    title = data['title']
    start_date_str = data['start_date']
    end_date_str = data.get('start_date', None)
    actor_id = data.get('actor.id', None)
    director_id = data.get('director.id', None)
    genre_id = data.get('genre.id', None)

    try:
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
    except ValueError:
        return jsonify ({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
        except ValueError:
            return jsonify ({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400

    # find by title if the tv_show alread exists
    existing_tv_show = TVShow.query.filter_by(title=title).first()

    # If tv_show already exists, return error
    if existing_tv_show:
        return jsonify ({"error": "TV Show already exists in database"}), 400
    
    # create new tv_show
    new_tv_show = TVShow(title=title, start_date=start_date, end_date=end_date)

    # if actor details were passed at creation, append
    if actor_id:
        actor = Actor.query.get(actor_id)
        if actor:
            new_tv_show.actors.append(actor)

    # if director details were passed at creation, append
    if director_id:
        director = Director.query.get(director_id)
        if director:
            new_tv_show.directors.append(director)

    if genre_id:
        genre = Genre.query.get(genre_id)
        if genre:
            new_tv_show.genres.append(genre)
    

    db.session.add(new_tv_show)
    db.session.commit()

    return jsonify (tvshow_schema.dump(new_tv_show))

# PUT endpoints
@tv_shows.route("/<int:id>/actor", methods=["PUT"])
@jwt_required()
def add_actor_to_tv_show(id):
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    actor_id = data.get('actor.id', None)

    if not actor_id:
        return jsonify ({"error": "Missing actor.id"}), 400
    
    actor = get_or_404(Actor, actor_id)
    
    tv_show.actors.append(actor)
    db.session.commit()

    return jsonify (tvshow_schema.dump(tv_show))

@tv_shows.route("/<int:id>/director", methods=["PUT"])
@jwt_required()
def add_director_to_tv_show(id):
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    director_id = data.get('director.id', None)

    if not director_id:
        return jsonify ({"error": "Missing director.id"}), 400
    
    director = get_or_404(Director, director_id)
    
    tv_show.directors.append(director)
    db.session.commit()

    return jsonify (tvshow_schema.dump(tv_show))

@tv_shows.route("/<int:id>/genre", methods=["PUT"])
@jwt_required()
def add_genre_to_tv_show(id):
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    genre_id = data.get('genre.id', None)

    if not genre_id:
        return jsonify ({"error": "Missing genre.id"}), 400
    
    genre = get_or_404(Genre, genre_id)
    
    tv_show.genres.append(genre)
    db.session.commit()

    return jsonify (tvshow_schema.dump(tv_show))

@tv_shows.route("/<int:id>/end_date", methods=["PUT"])
@jwt_required()
def add_end_date_to_tv_show(id):
    tv_show = get_or_404(TVShow, id)
    data = request.get_json()
    end_date_str = data.get('end_date', None)

    if not end_date_str:
        return jsonify ({"error": "Missing end_date"}), 400
    try:
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
    except ValueError:
        return jsonify ({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400
    
    tv_show.end_date = end_date
    db.session.commit()

    return jsonify (tvshow_schema.dump(tv_show))