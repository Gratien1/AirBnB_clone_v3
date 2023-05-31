#!/usr/bin/python3
"""GET, POST, PUT, DELETE on users"""
from api.v1.views import app_views
from models import storage
from datetime import datetime
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = storage.all("User")
    list_users = [user.to_dict()
                  for user in users.values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_user(user_id):
    """Retrieves a specific User"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_user(user_id):
    """Delete a specific User"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def add_a_user():
    """Add a user to storage"""
    from models.user import User
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    obj = User(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_a_user(user_id):
    """Update a specific User"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    static = ['id', 'email', 'created_at', 'updated_at']
    data_to_use = {k: v for k, v in data.items() if k not in static}
    k = "User" + "." + user_id
    if data_to_use:
        for d in data_to_use:
            setattr(storage.all()[k], d, data_to_use.get(d))
        setattr(storage.all()[k], 'updated_at', datetime.utcnow())
        storage.save()
    updated_user = storage.get("User", user_id)
    return jsonify(updated_user.to_dict())
