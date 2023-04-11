#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from os import getenv
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities_viewer():
    amenities_dict_list = []
    all_amenities = storage.all(Amenity)
    for amenity in all_amenities.values():
        amenities_dict_list.append(amenity.to_dict())
    return jsonify(amenities_dict_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_viewer(amenity_id):
    all_amenities = storage.all(Amenity)
    for amenity_key in all_amenities.keys():
        if amenity_key == f"Amenity.{amenity_id}":
            return jsonify(all_amenities[amenity_key].to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def detete_amenity(amenity_id):
    all_amenities = storage.all(Amenity)
    if f"Amenity.{amenity_id}" not in all_amenities.keys():
        abort(404)
    for amenity_key in all_amenities.keys():
        if amenity_key == f"Amenity.{amenity_id}":
            storage.delete(all_amenities[amenity_key])
            storage.save()
            return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "name" not in json_request.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**json_request)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    all_amenities = storage.all(Amenity)
    if f"Amenity.{amenity_id}" not in all_amenities.keys():
        abort(404)
    for key, value in json_request.items():
        setattr(all_amenities[f"Amenity.{amenity_id}"], key, value)
    all_amenities[f"Amenity.{amenity_id}"].save()
    return jsonify(all_amenities[f"Amenity.{amenity_id}"].to_dict()), 200
