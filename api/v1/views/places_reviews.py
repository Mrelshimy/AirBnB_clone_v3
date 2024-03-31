#!/usr/bin/python3
"""This module is the view of the reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews')
def get_reviews(place_id):
    """get all reviews in a place"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('reviews/<review_id>')
def get_review(review_id):
    """get a review by its Id"""
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete a review by its Id"""
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data.keys():
        return abort(400, 'Missing user_id')
    user = storage.get(User, data.get('user_id'))
    if not user:
        return abort(404)
    if 'text' not in data.keys():
        return abort(400, 'Missing text')
    review = Review(**data, place_id=place_id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update a review by id"""
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    data.pop('id', 0)
    data.pop('user_id', 0)
    data.pop('place_id', 0)
    data.pop('created_at', 0)
    data.pop('updated_at', 0)
    for key, value in data.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
