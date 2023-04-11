#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from os import getenv
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def place_by_city_viewer(city_id):
    if f"City.{city_id}" not in storage.all(City).keys():
        abort(404)
    places_dict_list = []
    all_places = storage.all(Place)
    for place_value in all_places.values():
        if place_value.city_id == city_id:
            places_dict_list.append(place_value.to_dict())
    return jsonify(places_dict_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place_viewer(place_id):
    all_places = storage.all(Place)
    for place_key in all_places.keys():
        if place_key == f"Place.{place_id}":
            return jsonify(all_places[place_key].to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def detete_place(place_id):
    all_places = storage.all(Place)
    if f"Place.{place_id}" not in all_places.keys():
        abort(404)
    for place_key in all_places.keys():
        if place_key == f"Place.{place_id}":
            storage.delete(all_places[place_key])
            storage.save()
            return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place_from_city(city_id):
    all_cities = storage.all(City)
    all_users = storage.all(User)
    if f"City.{city_id}" not in all_cities.keys():
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "user_id" not in json_request.keys():
        abort(400, "Missing user_id")
    if f"User.{json_request[user_id]}" not in all_users.keys():
        abort(404)
    if "name" not in json_request.keys():
        abort(400, "Missing name")
    new_place = Place(**json_request)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places", methods=['POST'],
                 strict_slashes=False)
def create_place():
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "name" not in json_request.keys():
        abort(400, "Missing name")
    new_place = Place(**json_request)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    all_places = storage.all(Place)
    if f"Place.{place_id}" not in all_places.keys():
        abort(404)
    for key, value in json_request.items():
        setattr(all_places[f"Place.{place_id}"], key, value)
    all_places[f"Place.{place_id}"].save()
    return jsonify(all_places[f"Place.{place_id}"].to_dict()), 200
