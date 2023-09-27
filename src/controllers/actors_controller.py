from flask import Blueprint, jsonify, request
from main import db
from models import Actor
from schemas import actors_list_schema, actor_schema
actors = Blueprint('actors', __name__, url_prefix="/actors")

#GET endpoints
@actors.route("/", methods=["GET"])
def get_actors():
    # route gets all the actors without delving into the nested fields
    # this will be handled when looking at the specific actor
    all_actors = Actor.query.all()
    result = actors_list_schema.dump(all_actors)
    return jsonify(result)

@actors.route("/<int:id>", methods=["GET"])
def get_actor(id):
    actor = Actor.query.get_or_404(id)
    result = actor_schema.dump(actor)
    return jsonify(result)