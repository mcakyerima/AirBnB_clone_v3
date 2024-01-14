#!/usr/bin/python3
"""Python flask script for crud operations on cities"""


from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        cities_list = [state_cities.to_dict() for state_cities in state.cities]
        return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is not None:
        city.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify)({"error": "Missing name"}, 400)
        city_object = request.get_json()
        new_city = City(**city_object)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'state_id', 'created_id', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict())
