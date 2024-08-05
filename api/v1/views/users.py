#!/usr/bin/python3
"""Creates a view for User objects that handles all
 default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, json, request, Response
import models
from models import storage


User = models.user.User


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """Retrieves a list of all User objects:
    GET /api/v1/users
    """
    users = list(storage.all(User).values())
    users_list = []
    if len(users):
        for user in users:
            users_list.append(user.to_dict())
    res = json.dumps(users_list, indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/users/<id>', strict_slashes=False)
def get_user(id):
    """Retrieves a single User object: GET /api/v1/users/<user_id>

    If the amenity_id is not linked to any User object, raises a 404 error
    """
    user = storage.get(User, id)
    if not user:
        abort(404)
    res = json.dumps(user.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    """Deletes a User object: DELETE /api/v1/users/<user_id>

     - If the user_id is not linked to any Amenity object,
       +raises a 404 error
     - Returns an empty dictionary with the status code 200
    """
    user = storage.get(User, id)
    if user is not None:
        user.delete()
        storage.save()
        storage.reload()
        res = json.dumps({}) + '\n'
        return Response(res, mimetype="application/json")
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User: POST /api/v1/users

    - uses request.get_json from Flask to transform the HTTP body
      + request to a dictionary
    - If the HTTP body request is not valid JSON, raises a
      +400 error with the message Not a JSON
    - If the dictionary doesn’t contain the key 'email', raises a 400 error
      +with the message 'Missing email'
    - If the dictionary doesn't contain the key 'password', raises a
      + 400 errow with the message 'Missing password'
    - Returns the new User with the status code 201
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    if not data or not len(data):
        abort(404)

    if not data.get("email"):
        abort(400, description="Missing email")
    if not data.get("password"):
        abort(400, description="Missing password")

    new_user = User(
        email=data.get('email'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last+name')
    )
    new_user.save()
    res = json.dumps(new_user.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json", status=201)


@app_views.route('/users/<string:id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(id):
    """Updates an Amenity object: PUT /api/v1/users/<user_id>

    - If the user_id is not linked to any City object, raise a 404 error
    - must use request.get_json from Flask to transform the HTTP body
      +request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400
      +error with the message 'Not a JSON'
    - Updates the User object with all key-value pairs of the dictionary.
    - Ignores keys: id, email, created_at and updated_at
    - Returns the User object with the status code 200
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    user = storage.get(User, id)
    if not user:
        abort(404)
    if data.get('first_name'):
        setattr(user, 'first_name', data['first_name'])
    if data.get('last_name'):
        setattr(user, 'last_name', data['last_name'])
    if data.get('password'):
        setattr(user, 'password', data['password'])
    user.save()
    res = json.dumps(user.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")
