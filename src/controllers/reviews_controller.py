from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from main import db, bcrypt
from models import User, Review, Movie, TVShow
from schemas import review_schema, reviews_schema

review = Blueprint('review', __name__, url_prefix="/review")

#POST endpoints
@review.route("/", methods=["POST"])
@jwt_required()
def new_review():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify({"error": "Please login before posting a review"}), 401

    data = request.get_json()
    if not data or data.get('content') is None:
        return jsonify({"error": "Missing review details"}), 400

    content = data['content']
    rating = data.get('rating', None)
    movie_id = data.get('movie.id', None)
    tv_id = data.get('tv_show.id', None)

    if movie_id is None and tv_id is None:
        return jsonify({"error": "You must link to either a movie or tv show at a minimum"}), 400
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

    # Pass new_review object to the dump method
    return jsonify(review_schema.dump(new_review))

@review.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def del_review(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return jsonify({"error": "Please login before deleting a review"}), 401
    
    review_to_delete = Review.query.get(id)
    if not review_to_delete:
        return jsonify ({"error": "Review not found"}), 404
    
    if review_to_delete.user_id != current_user.id:
        return jsonify ({"error": "Only the poster is allowed to remove their own review"}), 403
    
    db.session.delete(review_to_delete)
    db.session.commit()
    return jsonify ({"message": "Review has been successfully removed"})