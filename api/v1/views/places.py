#!/usr/bin/python3
"""app views blueprint places endpoints module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places(city_id):
    """Return list of all places in a city"""
    place_objs = storage.all(Place)
    places_list = []
    for value in place_objs.values():
        if value.city_id == city_id:
            places_list.append(Place.to_dict(value))
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False)
def place_id(place_id):
    """Return place data for endpoint /places/place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(Place.to_dict(place)), 200


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def place_id_delete(place_id):
    """Delete place for endpoint /places/place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def place_id_post(city_id):
    """adds new place within a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json:
        json_data = request.get_json()
        json_data["city_id"] = city_id
        if "user_id" in json_data:
            user = storage.get(User, json_data['user_id'])
            if user is None:
                abort(404)
            if "name" not in json_data:
                abort(400, "Missing name")
            new_place = Place(**json_data)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
        else:
            abort(400, "Missing user_id")
    else:
        abort(400, "Not a JSON")


@app_views.route("/places/<place_id>",
                 methods=['PUT'], strict_slashes=False)
def place_id_put(place_id):
    """update a plaxe with endpoint /places/<plae_id>"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json:
        json_data = request.get_json()
        for key, value in json_data.items():
            if key == "id" or key == "created_at" or key == "updated_at"\
                            or key == "user_id" or key == "city_id":
                continue
            setattr(place, key, value)
        storage.save()
        return jsonify(Place.to_dict(place)), 200
    else:
        abort(400, "Not a JSON")
