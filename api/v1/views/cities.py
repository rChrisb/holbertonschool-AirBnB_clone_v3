#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from os import getenv
from models.state import State
from models.city import City


# @app_views.route("/cities", methods=['GET'], strict_slashes=False)
# def cities_viewer():
#     cities_dict_list = []
#     all_cities = storage.all(City)
#     for city in all_cities.values():
#         cities_dict_list.append(city.to_dict())
#     return jsonify(cities_dict_list)


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def city_by_state_viewer(state_id):
    cities_dict_list = []
    all_cities = storage.all(City)
    for city_value in all_cities.values():
        if city_value.state_id == state_id:
            cities_dict_list.append(city_value.to_dict())
    return jsonify(cities_dict_list)
    abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def city_viewer(city_id):
    all_cities = storage.all(City)
    for city_key in all_cities.keys():
        if city_key == f"City.{city_id}":
            return jsonify(all_cities[city_key].to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def detete_city(city_id):
    all_cities = storage.all(City)
    if f"City.{city_id}" not in all_cities.keys():
        abort(404)
    for city_key in all_cities.keys():
        if city_key == f"City.{city_id}":
            storage.delete(all_cities[city_key])
            storage.save()
            return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city_from_state(state_id):
    all_states = storage.all(State)
    if f"State.{state_id}" not in all_states.keys():
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "name" not in json_request.keys():
        abort(400, "Missing name")
    new_city = City(**json_request)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities", methods=['POST'],
                 strict_slashes=False)
def create_city():
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "name" not in json_request.keys():
        abort(400, "Missing name")
    new_city = City(**json_request)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    all_cities = storage.all(City)
    if f"City.{city_id}" not in all_cities.keys():
        abort(404)
    for key, value in json_request.items():
        setattr(all_cities[f"City.{city_id}"], key, value)
    all_cities[f"City.{city_id}"].save()
    return jsonify(all_cities[f"City.{city_id}"].to_dict()), 200
