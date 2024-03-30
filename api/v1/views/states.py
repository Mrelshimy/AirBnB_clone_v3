#!/usr/bin/python3
"""app views blueprint states endpoints module"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states():
    """Return list of all states for endpoint /states"""
    states_objs = storage.all(State)
    states_list = []
    for value in states_objs.values():
        states_list.append(State.to_dict(value))
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def state_id(state_id):
    """Return state data for endpoint /states/state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(State.to_dict(state))


@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def state_id_delete(state_id):
    """Delete state for endpoint /states/state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})
