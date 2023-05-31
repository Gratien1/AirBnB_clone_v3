#!/usr/bin/python3
"""v1 starting point"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns v1 status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Returns storage stats"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
