#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from os import getenv
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_by_place_viewer(place_id):
    if f"Place.{place_id}" not in storage.all(Place).keys():
        abort(404)
    reviews_dict_list = []
    all_reviews = storage.all(Review)
    for review_value in all_reviews.values():
        if review_value.place_id == place_id:
            reviews_dict_list.append(review_value.to_dict())
    return jsonify(reviews_dict_list)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def review_viewer(review_id):
    all_reviews = storage.all(Review)
    for review_key in all_reviews.keys():
        if review_key == f"Review.{review_id}":
            return jsonify(all_reviews[review_key].to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def detete_review(review_id):
    all_reviews = storage.all(Review)
    if f"Review.{review_id}" not in all_reviews.keys():
        abort(404)
    for review_key in all_reviews.keys():
        if review_key == f"Review.{review_id}":
            storage.delete(all_reviews[review_key])
            storage.save()
            return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review_from_place(place_id):
    all_places = storage.all(Place)
    all_users = storage.all(User)
    if f"Place.{place_id}" not in all_places.keys():
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "user_id" not in json_request.keys():
        abort(400, "Missing user_id")
    if f"User.{json_request['user_id']}" not in all_users.keys():
        abort(404)
    if "text" not in json_request.keys():
        abort(400, "Missing text")
    new_review = Review(**json_request)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review():
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    if "name" not in json_request.keys():
        abort(400, "Missing name")
    new_review = Review(**json_request)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    json_request = request.get_json()
    if not json_request:
        abort(400, "Not a JSON")
    all_reviews = storage.all(Review)
    if f"Review.{review_id}" not in all_reviews.keys():
        abort(404)
    for key, value in json_request.items():
        setattr(all_reviews[f"Review.{review_id}"], key, value)
    all_reviews[f"Review.{review_id}"].save()
    return jsonify(all_reviews[f"Review.{review_id}"].to_dict()), 200
