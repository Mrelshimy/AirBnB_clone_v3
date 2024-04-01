#!/usr/bin/python3
"""This module is the view of the reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities')
def get_amenities(place_id):
    """get all amenities in a place"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """delete a place amenity by its Id"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)
    if amenity not in place.amenities:
        return abort(404)
    if not place.amenity_ids:
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def post_amenity(place_id, amenity_id):
    """create a new amenity"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    new_amenity = Amenity(id=amenity_id)
    if not place.amenity_ids:
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201
