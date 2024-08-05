#!/usr/bin/python3
"""A view for Amenities objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, json, request, Response
import models
from models import storage


Amenity = models.amenity.Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenities():
    """Retrieves a list of all Amenity objects:
    GET /api/v1/amenities
    """
    amenities = list(storage.all(Amenity).values())
    amenities_list = []
    if len(amenities):
        for amenity in amenities:
            amenities_list.append(amenity.to_dict())
    res = json.dumps(amenities_list, indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/amenities/<string:id>', strict_slashes=False)
def get_single_amenity(id):
    """Retrieves a single Amenity object: GET /api/v1/amenities/<amenity_id>

    If the amenity_id is not linked to any Amenity object, raises a 404 error
    """

    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    res = json.dumps(amenity.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/amenities/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(id):
    """Deletes an Amenity object: DELETE /api/v1/amenities/<amenity_id>

     - If the amenity_id is not linked to any Amenity object,
       +raises a 404 error
     - Returns an empty dictionary with the status code 200
    """
    amenity = storage.get(Amenity, id)
    if amenity is not None:
        amenity.delete()
        storage.save()
        storage.reload()
        res = json.dumps({}) + '\n'
        return Response(res, mimetype="application/json")
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity: POST /api/v1/amenities

    - uses request.get_json from Flask to transform the HTTP body
      + request to a dictionary
    - If the HTTP body request is not valid JSON, raises a
      +400 error with the message Not a JSON
    - If the dictionary doesn’t contain the key name, raises a 400 error
      +with the message Missing name
    - Returns the new State with the status code 201
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    if not data:
        abort(404)

    if not data.get('name'):
        abort(400, description="Missing name")

    new_amenity = Amenity(name=data.get('name'))
    new_amenity.save()
    res = json.dumps(new_amenity.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json", status=201)


@app_views.route('/amenities/<string:id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(id):
    """Updates an Amenity object: PUT /api/v1/amenities/<amenity_id>

    - If the amenity_id is not linked to any City object, raise a 404 error
    - must use request.get_json from Flask to transform the HTTP body
      +request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400
      +error with the message Not a JSON
    - Update the Amenity object with all key-value pairs of the dictionary.
    - Ignore keys: id, created_at and updated_at
    - Returns the Amenity object with the status code 200
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    if data.get('name'):
        setattr(amenity, 'name', data['name'])
        amenity.save()
    res = json.dumps(amenity.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")
