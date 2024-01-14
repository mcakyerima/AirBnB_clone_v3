#!/usr/bin/python3
"""Python flask script to create the Crud operations for amenity"""


from flask import Flask, jsonify, make_response, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """getting the amenities from the database"""
    amenities_dict = [amenity.to_dict() for amenity in storage.all(Amenity).
                      values()]
    return jsonify(amenities_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_byId(amenity_id):
    """getting the amenity by the id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amentity_id):
    amenity = storage.get(Amenity, amentity_id)
    if amenity is not None:
        amenity.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creating the new amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity_object = request.get_json()
    new_amenity = Amenity(**amenity_object)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        for k, v in request.get_json().items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict())
    else:
        abort(404)
