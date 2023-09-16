from flask import Blueprint, jsonify, request
from main import db
from models.actors import Actor

actors = Blueprint('actors', __name__, url_prefix="/actors")

#GET endpoints
@actors.route("/", methods=["GET"])
def get_actors():
    stmt = db.select(Actor)
    actors_list = db.session.scalars(stmt)
    # # Convert the actors from the database into a JSON format and store them is result
    # result = actors_schema.dump(actors_list)
    # # return the data in JSON format
    # return jsonify(result)
    return "List of actors"

@actors.route("/", methods=["POST"])
def create_actor():
    # # Create a new actor
    # actor_fields = actor_schema.load(request.json)

    # new_actor = Actor(**actor_fields)

    # db.session.add(new_actor)
    # db.session.commit()

    # return jsonify(actor_schema.dump(new_actor))
    return "Actor created"

@actors.route("/<int:id>/", methods=["DELETE"])
def delete_actor(id):
    # # Get the user id invoking get_jwt_identity
    # user_id = get_jwt_identity()
    # # Find in the database
    # stmt = db.select(User).filter_by(id=user_id)
    # user = db.session.scalar(stmt)
    # # Make sure user is in DB
    # if not user:
    #     return abort(401, description="Invalid user")
    # # Stop request is user is not admin
    # if not user.admin:
    #     return abort(401, description="Unauthorised user")
    # # find the actor
    # stmt = db.select(Actor).filter_by(id=id)
    # actor = db.session.scalar(stmt)
    # # handle error if actor does not exist
    # if not actor:
    #     return abort(400, description="Actor does not exist")
    # # delete the actor
    # db.session.delete(actor)
    # db.session.commit
    # # return the actor in response
    # return jsonify(actor_scehma.dump(actor))
    return "Actor Deleted"