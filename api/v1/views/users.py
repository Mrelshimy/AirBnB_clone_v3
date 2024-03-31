#!/usr/bin/python3
"""This module is the view of the users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('users')
def get_users():
    """get all users from storage"""
    all = storage.all(User)
    users = [user.to_dict() for user in all.values()]
    return jsonify(users)


@app_views.route('users/<user_id>')
def get_user(user_id):
    """get a user by its Id"""
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete a user by its Id"""
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('users', methods=['POST'])
def create_user():
    """create a new user"""
    if not request.is_json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data.keys():
        return abort(400, 'Missing email')
    if 'password' not in data.keys():
        return abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update a user by id"""
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    if not request.is_json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    data.pop('id', 0)
    data.pop('email', 0)
    data.pop('created_at', 0)
    data.pop('updated_at', 0)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
