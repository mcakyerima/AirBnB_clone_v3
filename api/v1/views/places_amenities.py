#!/usr/bin/python3
"""
python flask script to create crud operations for
place_amenities
"""


from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_idct() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in amenities:
        abort(404)
    amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
           strict_slashes=False)
def createPlace_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in amenities:
        return (jsonify(amenity.to_dict()), 200)
    amenities.append(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)
