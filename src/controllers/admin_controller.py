from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models import User, Actor, Director, Movie, TVShow, Review, Genre
from schemas import users_list_schema

admin = Blueprint('admin', __name__, url_prefix="/admin")

#GET endpoints
@admin.route("/user", methods=["GET"])
@jwt_required()
def get_users():
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # if passed, provide the list of users
    all_users = User.query.all()
    result = users_list_schema.dump(all_users)
    return jsonify(result)

# DELETE endpoints
@admin.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
def del_users(id):
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    user = User.query.get(id)
    if not user:
        return jsonify ({"error": "User not found"}), 404
    if current_user == user:
        return jsonify ({"error": "you cannot remove yourself through admin dashboard, please delete yourself through user dashboard"}), 403
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"You have removed user: {user.username} successfully."}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the user, reason: {str(e)}"}), 500
    
@admin.route("/actor/<int:id>", methods=["DELETE"])
@jwt_required()
def del_actor(id):
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    actor = Actor.query.get(id)
    if not actor:
        return jsonify ({"error": "Actor not found"}), 404
    
    try:
        db.session.delete(actor)
        db.session.commit()
        return jsonify({"message": f"You have removed actor: {actor.name} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the actor, reason: {str(e)}"}), 500
    
@admin.route("/director/<int:id>", methods=["DELETE"])
@jwt_required()
def del_director(id):
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    director = Director.query.get(id)
    if not director:
        return jsonify ({"error": "Director not found"}), 404
    
    try:
        db.session.delete(director)
        db.session.commit()
        return jsonify({"message": f"You have removed director: {director.name} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the director, reason: {str(e)}"}), 500
    
@admin.route("/genre/<int:id>", methods=["DELETE"])
@jwt_required()
def del_genre(id):
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    genre = Genre.query.get(id)
    if not genre:
        return jsonify ({"error": "Genre not found"}), 404
    
    try:
        db.session.delete(genre)
        db.session.commit()
        return jsonify({"message": f"You have removed genre: {genre.name} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the genre, reason: {str(e)}"}), 500
    
@admin.route("/movie/<int:id>", methods=["DELETE"])
@jwt_required()
def del_movie(id):
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    movie = Movie.query.get(id)
    if not movie:
        return jsonify ({"error": "Movie not found"}), 404
    
    try:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": f"You have removed movie: {movie.title} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the movie, reason: {str(e)}"}), 500
    
@admin.route("/tv_show/<int:id>", methods=["DELETE"])
@jwt_required()
def del_tv_show(id):
    # get id of current user from JWT
    user_id = get_jwt_identity()
    # get user from database
    current_user = User.query.get(user_id)
    # check if they are a user of the platform
    if not current_user:
        return jsonify({"error": "You are not registered or not logged in"}), 401
    # check if they are admin
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    tv_show = TVShow.query.get(id)
    if not tv_show:
        return jsonify ({"error": "TV Show not found"}), 404
    
    try:
        db.session.delete(tv_show)
        db.session.commit()
        return jsonify({"message": f"You have removed tv_show: {tv_show.title} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the tv_show, reason: {str(e)}"}), 500