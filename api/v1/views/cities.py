#!/usr/bin/python3
"""GET, POST, PUT, DELETE on cities"""
from api.v1.views import app_views
from models import storage
from datetime import datetime
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_of_state(state_id):
    """Retrieves the list of all City objects of a State"""
    if not storage.get("State", state_id):
        abort(404)
    cities = storage.all("City")
    list_cities = [city.to_dict()
                   for city in cities.values()
                   if city.state_id == state_id]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_city(city_id):
    """Retrieves a specific City"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_city(city_id):
    """Delete a specific City"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_a_city(state_id):
    """Add a city related a state to storage"""
    from models.city import City
    if not storage.get("State", state_id):
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    data['state_id'] = state_id
    obj = City(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_city(city_id):
    """Update a specific City"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    static = ['id', 'state_id', 'created_at', 'updated_at']
    data_to_use = {k: v for k, v in data.items() if k not in static}
    k = "City" + "." + city_id
    if data_to_use:
        for d in data_to_use:
            setattr(storage.all()[k], d, data_to_use.get(d))
        setattr(storage.all()[k], 'updated_at', datetime.utcnow())
        storage.save()
    updated_city = storage.get("City", city_id)
    return jsonify(updated_city.to_dict()), 200
