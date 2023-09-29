from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from main import db
from models import User, Review, Movie, TVShow
from schemas import review_schema
from .utils import get_or_404, get_current_user

review = Blueprint('review', __name__, url_prefix="/review")

#POST endpoint
@review.route("/", methods=["POST"])
@jwt_required()
def new_review():
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    data = request.get_json()
    if not data or data.get('content') is None:
        return jsonify({"error": "Missing review details"}), 400
    content = data['content']
    rating = data.get('rating', None)
    movie_id = data.get('movie.id', None)
    tv_id = data.get('tv_show.id', None)
    if movie_id is None and tv_id is None:
        return jsonify({"error": "You must link to either a movie or tv show at a minimum, use 'movie.id' or 'tv_show.id'"}), 400
    if movie_id is not None and tv_id is not None:
        return jsonify({"error": "You cannot have a review for a movie and a TV show at the same time"}), 400
    if rating is not None and (rating < 1 or rating > 5):
        return jsonify({"error": "Please list your rating from 1 to 5 only"}), 400
    new_review = Review(content=content, user_id=current_user.id, rating=rating)
    if movie_id is not None:
        movie = Movie.query.get(movie_id)
        if movie:
            new_review.movie_id = movie.id  # Use the ID of the Movie object
    if tv_id is not None:
        tv_show = TVShow.query.get(tv_id)
        if tv_show:
            new_review.tv_id = tv_show.id  # Use the ID of the TVShow object
    db.session.add(new_review)
    db.session.commit()
    return jsonify(review_schema.dump(new_review))

# DELETE endpoint
@review.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def del_review(id):
    current_user, error, status_code = get_current_user()
    if error:
        return error, status_code
    review_to_delete = get_or_404(Review, id)
    if review_to_delete.user_id != current_user.id:
        return jsonify ({"error": "Only the poster is allowed to remove their own review"}), 403
    db.session.delete(review_to_delete)
    db.session.commit()
    return jsonify ({"message": "Review has been successfully removed"})