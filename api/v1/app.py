#!/usr/bin/python3
"""API app for AirBnB project"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_database_connection(exception=None):
    """Close session"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=int(getenv('HBNB_API_PORT') or 5000),
            threaded=True)
