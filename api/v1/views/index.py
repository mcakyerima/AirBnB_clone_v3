#!/usr/bin/python3
"""
return a json string from a view using jsonify from
flask module
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returning the json string"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count_objects():
    """Couniting objects of each instance"""
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})
