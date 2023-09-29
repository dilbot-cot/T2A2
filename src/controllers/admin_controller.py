from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from main import db
from models import User, Actor, Director, Movie, TVShow, Review, Genre
from schemas import users_list_schema
from .utils import get_or_404, get_current_user

admin = Blueprint('admin', __name__, url_prefix="/admin")

# Each method requires the user to first be logged in, then checks if they are an admin

# GET method
@admin.route("/user", methods=["GET"])
@jwt_required()
# Get all users details (exclude passwords)
def get_users():
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    
    all_users = User.query.all()
    result = users_list_schema.dump(all_users)
    return jsonify(result)

# PUT method
@admin.route("/user/<int:id>", methods=["PUT"])
@jwt_required()
# Make another user an admin
def make_user_admin(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # return 404 error if the user to update doesn't exist
    user = get_or_404(User, id)
    data = request.get_json()
    update_admin = data.get('is_admin', None)
    # try to update, but if the is_admin field is not  boolean return error
    try:
        if not isinstance(update_admin, bool):
            raise ValueError("'is_admin' must be a boolean")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    user.is_admin = update_admin
    db.session.commit()
    return jsonify ({"message": f"User: '{user.username}' has had 'is_admin' permissions changed to '{update_admin}'"})

# DELETE methods
@admin.route("/user/<int:id>", methods=["DELETE"])
# delete a user
@jwt_required()
def del_users(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the user exists
    user = get_or_404(User, id)
    # checks if they are attempting to remove themselves in the admin dashboard
    if current_user == user:
        return jsonify ({"error": "you cannot remove yourself through admin dashboard, please delete yourself through user dashboard"}), 403
    # attempt to delete the user, if an error occurs, return the exception
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"You have removed user: {user.username} successfully."}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the user, reason: {str(e)}"}), 500
    
@admin.route("/actor/<int:id>", methods=["DELETE"])
@jwt_required()
def del_actor(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the actor exists
    actor = get_or_404(Actor, id)
    # attempt to delete the actor, if an error occurs, return the exception
    try:
        db.session.delete(actor)
        db.session.commit()
        return jsonify({"message": f"You have removed actor: {actor.name} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the actor, reason: {str(e)}"}), 500
    
@admin.route("/director/<int:id>", methods=["DELETE"])
@jwt_required()
def del_director(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the director exists
    director = get_or_404(Director, id)
    # attempt to delete the director, if an error occurs, return the exception
    try:
        db.session.delete(director)
        db.session.commit()
        return jsonify({"message": f"You have removed director: {director.name} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the director, reason: {str(e)}"}), 500
    
@admin.route("/genre/<int:id>", methods=["DELETE"])
@jwt_required()
def del_genre(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the genre exists
    genre = get_or_404(Genre, id)
    # attempt to delete the genre, if an error occurs, return the exception
    try:
        db.session.delete(genre)
        db.session.commit()
        return jsonify({"message": f"You have removed genre: {genre.name} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the genre, reason: {str(e)}"}), 500
    
@admin.route("/movie/<int:id>", methods=["DELETE"])
@jwt_required()
def del_movie(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the movie exists
    movie = get_or_404(Movie, id)
    # attempt to delete the movie, if an error occurs, return the exception
    try:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": f"You have removed movie: {movie.title} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the movie, reason: {str(e)}"}), 500
    
@admin.route("/tv_show/<int:id>", methods=["DELETE"])
@jwt_required()
def del_tv_show(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the TV Show exists
    tv_show = get_or_404(TVShow, id)
    # attempt to delete the TV Show, if an error occurs, return the exception
    try:
        db.session.delete(tv_show)
        db.session.commit()
        return jsonify({"message": f"You have removed tv_show: {tv_show.title} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the tv_show, reason: {str(e)}"}), 500
    
@admin.route("/review/<int:id>", methods=["DELETE"])
@jwt_required()
def del_review(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    if not current_user.is_admin:
        return jsonify({"error": "You do not have permission to perform this function"}), 403
    # check if the review exists
    review = get_or_404(Review, id)
    # attempt to delete the review, if an error occurs, return the exception
    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": f"You have removed review {review.id} successfully"}), 200
    except Exception as e:
        return jsonify ({"error": f"An error occured while attempting to delete the review, reason: {str(e)}"}), 500