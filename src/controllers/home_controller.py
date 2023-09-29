from flask import Blueprint, jsonify

home = Blueprint('home', __name__, url_prefix="/")

@home.route("/", methods=["GET"])
def hello_world():
    return jsonify ({
        "Actions": "You can select from the following endpoints",
        "ADMIN": {
            "GET a list of all users": "'admin/user' must be logged in as administrator",
            "PUT to change a users administartion permissions": "'admin/user/<id>' must be logged in as administrator, required fields 'is_admin'",
            "DELETE a user": "'admin/user/<id>' must be logged in as administrator",
            "DELETE a actor": "'admin/actor/<id>' must be logged in as administrator",
            "DELETE a director": "'admin/director/<id>' must be logged in as administrator",
            "DELETE a genre": "'admin/genre/<id>' must be logged in as administrator",
            "DELETE a movie": "'admin/movie/<id>' must be logged in as administrator",
            "DELETE a TV Show": "'admin/tv_show/<id>' must be logged in as administrator",
            "DELETE a review": "'admin/review/<id>' must be logged in as administrator"
        },
        "ACTORS": {
            "List all actors": "'actors/'",
            "List specific actor details": "'actors/<id>'",
            "POST a new actor": "'actors/' must be logged in as user, mandatory fields: 'name', 'dob' optional fields: 'movie.id', 'tv_show.id'",
            "PUT a movie relationship": "'actors/<id>/movie' must be logged in as a user, mandatory fields: 'movie.id'",
            "PUT a TV Show relationship": "'actors/<id>/tv' must be logged in as a user, mandatory fields: 'tv_show.id'",
        },
        "DIRECTORS": {
            "List all directors": "'directors/'",
            "List specific director details": "'directors/<id>'",
            "POST a new director": "'directors/' must be logged in as user, mandatory fields: 'name', 'dob' optional fields: 'movie.id', 'tv_show.id'",
            "PUT a movie relationship": "'directors/<id>/movie' must be logged in as a user, mandatory fields: 'movie.id'",
            "PUT a TV Show relationship": "'directors/<id>/tv' must be logged in as a user, mandatory fields: 'tv_show.id'",
        },
        "GENRES": {
            "List all Genres": "'genres/'",
            "List specific actor details": "'genres/<id>'",
            "POST a new genre": "'genres/' must be logged in as user, mandatory fields: 'name'"
        },
        "MOVIES": {
            "List all movies": "'movies/'",
            "List specific movie details": "'movies/<id>'",
            "POST a new movie": "'movies/' must be logged in as user, mandatory fields: 'title', 'release_date' optional fields: 'actor.id', 'director.id', 'genre.id'",
            "PUT an actor relationship": "'movies/<id>/actor' must be logged in as user, mandatory fields: 'actor.id'",
            "PUT a director relationship": "'movies/<id>/director' must be logged in as user, mandatory fields: 'director.id'",
            "PUT a genre relationship": "'movies/<id>/genre' must be logged in as user, mandatory fields: 'genre.id'"
        },
        "TV SHOWS": {
            "List all TV Shows": "'tv_shows/'",
            "List specific TV Show details": "'tv_shows/<id>'",
            "POST a new TV Show": "'tv_shows/' must be logged in as user, mandatory fields: 'title', 'start_date' optional fields: 'end_date', 'actor.id', 'director.id', 'genre.id'",
            "PUT an actor relationship": "'tv_shows/<id>/actor' must be logged in as user, mandatory fields: 'actor.id'",
            "PUT a director relationship": "'tv_shows/<id>/director' must be logged in as user, mandatory fields: 'director.id'",
            "PUT a genre relationship": "'tv_shows/<id>/genre' must be logged in as user, mandatory fields: 'genre.id'",
            "PUT an end date": "'tv_shows/<id>/end_date' must be logged in as user, mandatory fields: 'end_date'"
        },
        "USERS": {
            "POST a new user": "'user/reg' mandatory fields: 'username', 'email', 'password'",
            "POST a login (to obtain bearer token)": "'user/auth' mandatory fields: 'username', 'password'",
            "GET all reviews written": "'user/reviews' must be logged in as user",
            "DELETE self": "'user/' must be logged in"
        },
        "REVIEWS": {
            "POST a new review": "'review/' must be logged in, mandaotry fields: 'content', mandatory exclusivly 'movie.id' or 'tv_show.id' optional field: 'rating'",
            "DELETE a posted review": "'review/<id>' must be logged in"
        },
    })