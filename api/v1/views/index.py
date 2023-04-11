#!/usr/bin/python3
"""return status OK in json format"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


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
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        })
