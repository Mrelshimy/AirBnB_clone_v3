#!/usr/bin/python3
"""This module is the view of the cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities')
def get_cities(state_id):
    """get all cities in a state"""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('cities/<city_id>')
def get_city(city_id):
    """get a city by its Id"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a city by its Id"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data.keys():
        return abort(400, 'Missing name')
    city = City(name=data['name'], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city by id"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    data.pop('id', 0)
    data.pop('state_id', 0)
    data.pop('created_at', 0)
    data.pop('updated_at', 0)
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
