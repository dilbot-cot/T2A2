from flask import jsonify
from main import db

def get_or_404(model, id):
    resource = model.query.get(id)
    if not resource:
        raise ValueError(f"{model.__name__} not found")  # Raise an exception
    return resource