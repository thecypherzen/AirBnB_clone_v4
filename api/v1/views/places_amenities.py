#!/usr/bin/python3
"""Creates a view for a Place object's Amenities that handles all
 default RESTFul API actions.

 - Depending of the storage:
   -> DBStorage: list, create and delete Amenity objects from amenities
      +relationship
   -> FileStorage: list, add and remove Amenity ID in the list
      +amenity_ids of a Place object
"""

from api.v1.views import app_views
from flask import abort, json, Response
import models
from models import storage
from os import getenv


Amenity = models.amenity.Amenity
Place = models.place.Place
db_mode = models.storage_t


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves a list of all Amenities objects of a Place:
    GET /api/v1/places/<place_id>/amenities

    - If the place_id is not linked to any Place object, raises a 404 error
    """
    # check if place_id matches a valid place
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # get amenities of the place object
    if db_mode == "db":
        s_amenities = place.amenities
    else:
        s_amenities = [storage.get(Amenity, amenity_id)
                       for amenity_id in place.amenity_ids]
    # prepare amenities list and return
    amenities = []
    for amenity in s_amenities:
        amenities.append(amenity.to_dict())
    res = json.dumps(amenities, indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object of a Place:
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id>

     - If the place_id is not linked to any Place object,
       +raises a 404 error
     - If the amenity_id is not linked to any Amenity object,
       +raises a 404 error
     - If the Amenity is not linked to the Place before the request,
       +raises a 404 error
     - Returns an empty dictionary with the status code 200
    """
    # check if place_id and amenity_id match a Place and Amenity
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not all([place, amenity]):
        abort(404)

    # delete amenity from place's amenities if they'e linked and commit
    # if using db or file_storage
    if db_mode == "db":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            place.save()
            storage.reload()
    else:
        if amenity.id in place.amenity_ids:
            place.amenity_ids.remove(amenity.id)
            place.save()
            storage.reload()
    # prepare response and return
    res = json.dumps({}) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place:
       POST /api/v1/places/<place_id>/amenities/<amenity_id>

    - No HTTP body needed
    - If the place_id is not linked to any Place object, raise a 404 error
    - If the amenity_id is not linked to any Amenity object, raise a 404 error
    - If the Amenity is already linked to the Place, return the Amenity with
      + the status code 200
    - Returns the Amenity with the status code 201
    """
    # check if place_id and amenity_id both have valid Objects
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not all([place, amenity]):
        abort(404)
    # get place's amenities list
    status = 201
    if db_mode == "db":
        # link amenity to place if not already linked
        if amenity in place.amenities:
            status = 200
        else:
            place.amenities.append(amenity)
            place.save()
    else:
        if amenity.id in place.amenity_ids:
            status = 200
        else:
            place.amenity_ids.apend(amenity.id)
            place.save()
    # return amenity
    res = json.dumps(amenity.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json", status=status)
