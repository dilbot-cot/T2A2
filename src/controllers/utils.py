from flask import request, jsonify
from datetime import datetime
from main import db
from flask_jwt_extended import get_jwt_identity
from models import User

# retrieve a resource by its ID or return a 404 error
def get_or_404(model, id):
    resource = model.query.get(id)
    if not resource:
        raise ValueError(f"{model.__name__} not found")
    return resource

# validate a JSON payload and check for any missing required fields
def validate_json_fields(required_fields):
    data = request.get_json()
    if not data:
        return None, jsonify({"error": "No JSON payload"}), 400

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return None, jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    
    return data, None, None

# Parse a date string in d/m/yy to a python date object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date(), None, None
    except ValueError:
        return None, jsonify({"error": "Invalid date format. Please input as 'dd/mm/yyyy'"}), 400
    
# Append a related object to a resource for database models
def append_relation_to_resource(resource, relation_id, append_function):
    append_function(resource, relation_id)

# Adds the resource to the database, commit the change and respond with a message
def commit_and_respond(resource, schema):
    db.session.add(resource)
    db.session.commit()
    return jsonify(schema.dump(resource))

# Retrieve the current logged in user
def get_current_user():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user:
        return None, jsonify({"error": "You are not authorised to perform this action, please login first"}), 401
    return current_user, None, None