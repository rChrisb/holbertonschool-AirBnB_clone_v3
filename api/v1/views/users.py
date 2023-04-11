#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from os import getenv
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def users_viewer():
    users_dict_list = []
    all_users = storage.all(User)
    for user in all_users.values():
        users_dict_list.append(user.to_dict())
    return jsonify(users_dict_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def user_viewer(user_id):
    all_users = storage.all(User)
    for user_key in all_users.keys():
        if user_key == f"User.{user_id}":
            return jsonify(all_users[user_key].to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def detete_user(user_id):
    all_users = storage.all(User)
    if f"User.{user_id}" not in all_users.keys():
        abort(404)
    for user_key in all_users.keys():
        if user_key == f"User.{user_id}":
            storage.delete(all_users[user_key])
            storage.save()
            return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_user():
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "email" not in json_request.keys()
    or "password" not in json_request.keys():
        abort(400, "Missing name")
    new_user = User(**json_request)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    all_users = storage.all(User)
    if f"User.{user_id}" not in all_users.keys():
        abort(404)
    for key, value in json_request.items():
        setattr(all_users[f"User.{user_id}"], key, value)
    all_users[f"User.{user_id}"].save()
    return jsonify(all_users[f"User.{user_id}"].to_dict()), 200
