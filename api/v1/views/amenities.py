#!/usr/bin/python3
"""GET, POST, PUT, DELETE on amenities"""
from api.v1.views import app_views
from models import storage
from datetime import datetime
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all("Amenity")
    list_amenities = [amenity.to_dict()
                      for amenity in amenities.values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_amenity(amenity_id):
    """Retrieves a specific Amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_amenity(amenity_id):
    """Delete a specific Amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def add_a_amenity():
    """Add an amenity to storage"""
    from models.amenity import Amenity
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    obj = Amenity(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_a_amenity(amenity_id):
    """Update a specific Amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    static = ['id', 'created_at', 'updated_at']
    data_to_use = {k: v for k, v in data.items() if k not in static}
    k = "Amenity" + "." + amenity_id
    if data_to_use:
        for d in data_to_use:
            setattr(storage.all()[k], d, data_to_use.get(d))
        setattr(storage.all()[k], 'updated_at', datetime.utcnow())
        storage.save()
    updated_amenity = storage.get("Amenity", amenity_id)
    return jsonify(updated_amenity.to_dict())
