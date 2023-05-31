#!/usr/bin/python3
"""GET, POST, PUT, DELETE on states"""
from api.v1.views import app_views
from models import storage
from datetime import datetime
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all("State")
    list_states = [state.to_dict() for state in states.values()]
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_a_state(state_id):
    """Retrieves a specific State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_state(state_id):
    """Delete a specific State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_a_state():
    from models.state import State
    """Add a state to storage"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    obj = State(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_a_state(state_id):
    """Update a specific State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    static = ['id', 'created_at', 'updated_at']
    data_to_use = {k: v for k, v in data.items() if k not in static}
    k = "State" + "." + state_id
    if data_to_use:
        for d in data_to_use:
            setattr(storage.all()[k], d, data_to_use.get(d))
        setattr(storage.all()[k], 'updated_at', datetime.utcnow())
        storage.save()
    storage.save()
    updated_state = storage.get("State", state_id)
    return jsonify(updated_state.to_dict()), 200
