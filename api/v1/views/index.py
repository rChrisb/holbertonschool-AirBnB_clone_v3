#!/usr/bin/python3
"""return status OK in json format"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def json_status():
    """retruns status"""
    return jsonify({
        "status": "OK"
        })


@app_views.route('/stats')
def number_by_type():
    """count number of object by class"""
    return jsonify({
        "amenities": f"{storage.count(Amenity)}",
        "cities": f"{storage.count(City)}",
        "places": f"{storage.count(Place)}",
        "reviews": f"{storage.count(Review)}",
        "states": f"{storage.count(States)}",
        "users": f"{storage.count(User)}"
        })
