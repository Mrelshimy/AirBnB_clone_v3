#!/usr/bin/python3
"""app views blueprint amenities endpoints module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenities():
    """Return list of all amenities for endpoint /amenities"""
    amenities_objs = storage.all(Amenity)
    amenities_list = []
    for value in amenities_objs.values():
        amenities_list.append(Amenity.to_dict(value))
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def amenity_id(amenity_id):
    """Return amenity data for endpoint /amenities/amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(Amenity.to_dict(amenity)), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def amenity_id_delete(amenity_id):
    """Delete amenity for endpoint /amenities/amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def amenity_id_post():
    """adds new amenity with endpoint /amenities"""
    if request.is_json:
        json_data = request.get_json()
        if "name" in json_data:
            new_amenity = Amenity(**json_data)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>",
                 methods=['PUT'], strict_slashes=False)
def amenity_id_put(amenity_id):
    """update a amenity with endpoint /amenities/<amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.is_json:
        json_data = request.get_json()
        for key, value in json_data.items():
            if key == "id" or key == "created_at" or key == "updated_at":
                continue
            setattr(amenity, key, value)
        storage.save()
        return jsonify(Amenity.to_dict(amenity)), 200
    else:
        abort(400, "Not a JSON")
