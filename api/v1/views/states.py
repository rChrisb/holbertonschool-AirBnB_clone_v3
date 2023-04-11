#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states_viewer():
    states_dict_list = []
    all_states = storage.all(State)
    for state in all_states.values():
        states_dict_list.append(state.to_dict())
    return jsonify(states_dict_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_viewer(state_id):
    all_states = storage.all(State)
    for state_key in all_states.keys():
        if state_key == f"State.{state_id}":
            return jsonify(all_states[state_key].to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def detete_state(state_id):
    all_states = storage.all(State)
    if f"State.{state_id}" not in all_states.keys():
        abort(404)
    for state_key in all_states.keys():
        if state_key == f"State.{state_id}":
            storage.delete(all_states[state_key])
            storage.save()
            return jsonify({}), 200


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def create_state():
    json_request = request.get_json()
    if not json_request:
        abort(404, "Not a JSON")
    if "name" not in json_request.keys():
        abort(404, "Missing name")
    new_state = State(**json_request)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    json_request = request.get_json()
    if not json_request:
        abort(404, "Not a JSON")
    all_states = storage.all(State)
    if f"State.{state_id}" not in all_states.keys():
        abort(404)
    all_states[f"State.{state_id}"].__dict__.update(json_request)
    all_states[f"State.{state_id}"].save()
    return jsonify(all_states[f"State.{state_id}"].to_dict()), 200
