#!/usr/bin/python3
"""A view for Cities objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, json, request, Response
import models
from models import storage

City = models.city.City
State = models.state.State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves list of all City objects of a State:
    GET /api/v1/states/<state_id>/cities

    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    res = json.dumps(cities, indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/cities/<string:id>', strict_slashes=False)
def get_single_city(id):
    """Retrieves a single City object. : GET /api/v1/cities/<city_id>

    If the city_id is not linked to any City object, raises a 404 error
    """

    city = storage.get(City, id)
    if not city:
        abort(404)
    res = json.dumps(city.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/cities/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_single_city(id):
    """Deletes a City object: DELETE /api/v1/cities/<city_id>

     - If the city_id is not linked to any City object, raises a 404 error
     - Returns an empty dictionary with the status code 200
    """
    city = storage.get(City, id)
    if city is not None:
        city.delete()
        storage.save()
        storage.reload()
        res = json.dumps({}) + '\n'
        return Response(res, mimetype="application/json")
    abort(404)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new City

    - uses request.get_json from Flask to transform the HTTP body
      + request to a dictionary
    - If the state_id is not linked to any State object, raises a 404 error
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

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_city = City(name=data.get('name'),
                    state_id=state_id)
    new_city.save()
    res = json.dumps(new_city.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json", status=201)


@app_views.route('/cities/<string:id>', methods=['PUT'], strict_slashes=False)
def update_city(id):
    """Updates a City object: PUT /api/v1/cities/<city_id>

    - If the state_id is not linked to any City object, raise a 404 error
    - must use request.get_json from Flask to transform the HTTP body
      +request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400
      +error with the message Not a JSON
    - Update the City object with all key-value pairs of the dictionary.
    - Ignore keys: id, created_at and updated_at
    - Returns the State object with the status code 200
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    city = storage.get(City, id)
    if not city:
        abort(404)
    if data.get('name'):
        setattr(city, 'name', data['name'])
    if data.get('state_id'):
        setattr(city, 'state_id', data['state_id'])
    city.save()
    res = json.dumps(city.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")
