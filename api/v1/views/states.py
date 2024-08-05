#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, json, request, Response
import models
from models import storage

State = models.state.State


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    states = storage.all(State)
    response = []
    for state in states.values():
        response.append(state.to_dict())
    res = json.dumps(response, indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/states/<string:id>', strict_slashes=False)
def get_single_state(id):
    """Retrieves a single State object: GET /api/v1/states/<state_id>"""

    state = storage.get(State, id)
    if not state:
        abort(404)
    res = json.dumps(state.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/states/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_single_state(id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>

     - If the state_id is not linked to any State object, raise a 404 error
     - Returns an empty dictionary with the status code 200
    """
    state = storage.get(State, id)
    if state is not None:
        state.delete()
        storage.save()
        storage.reload()
        res = json.dumps({}) + '\n'
        return Response(res, mimetype="application/json")
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State

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
    if not data or not data.get("name"):
        abort(400, description="Missing name")
    new_state = State(name=data.get("name"))
    new_state.save()
    res = json.dumps(new_state.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json", status=201)


@app_views.route('/states/<string:id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    """Updates a State object: PUT /api/v1/states/<state_id>

    - If the state_id is not linked to any State object, raise a 404 error
    - must use request.get_json from Flask to transform the HTTP body
      +request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400
      +error with the message Not a JSON
    - Update the State object with all key-value pairs of the dictionary.
    - Ignore keys: id, created_at and updated_at
    - Returns the State object with the status code 200
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    state = storage.get(State, id)
    if not state:
        abort(404)
    name = data.get('name')
    if name:
        setattr(state, 'name', name)
        state.save()
    res = json.dumps(state.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")
