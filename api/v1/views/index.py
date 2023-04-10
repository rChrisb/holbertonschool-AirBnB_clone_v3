#!/usr/bin/python3
"""return status OK in json format"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def json_status():
    return jsonify({
        "status": "OK"
        })


@app_views.route('/api/v1/stats') 
def number_by_type():
    return jsonify({
        "amenities": f"{storage.count(Amenity)}"
        "cities": f"{storage.count(City)}"
        "reviews": f"{storage.count(Review)}"
        "states": f"{storage.count(States)}"
        "users": f"{storage.count(User)}"
        })
