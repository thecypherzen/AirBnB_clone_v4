#!/usr/bin/python3
"""Creates a view for Review objects that handles all
 default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, json, request, Response
import models
from models import storage


Place = models.place.Place
User = models.user.User
Review = models.review.Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves a list of all Review objects of a Place:
    GET /api/v1/places/<place_id>/reviews

    - If the place_id is not linked to any Place object, raises a 404 error
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = []
    if len(place.reviews):
        for review in place.reviews:
            reviews.append(review.to_dict())
    res = json.dumps(reviews, indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/reviews/<rev_id>', strict_slashes=False)
def get_review(rev_id):
    """Retrieves a single Review object: GET /api/v1/reviews/<review_id>

    If the review_id is not linked to any Review object, raises a 404 error
    """
    review = storage.get(Review, rev_id)
    if not review:
        abort(404)
    res = json.dumps(review.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")


@app_views.route('/reviews/<rev_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(rev_id):
    """Deletes a Review object: DELETE /api/v1/reviews/<review_id>

     - If the review_id is not linked to any Review object,
       +raises a 404 error
     - Returns an empty dictionary with the status code 200
    """
    review = storage.get(Review, rev_id)
    if review is not None:
        review.delete()
        storage.save()
        storage.reload()
        res = json.dumps({}) + '\n'
        return Response(res, mimetype="application/json")
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review of a Place: POST /api/v1/places/<place_id>/reviews

    - uses request.get_json from Flask to transform the HTTP body
      + request to a dictionary
    - If the HTTP body request is not valid JSON, raises a
      +400 error with the message Not a JSON
    - If the dictionary doesn’t contain the key 'user_id', raises a 400 error
      +with the message 'Missing user_id'
    - If the user_id is not linked to any User object, raise a 404 error
    - If the place_id is not linked to any Place object, raise a 404 error
    - If the dictionary doesn't contain the key 'text', raises a
      + 400 errow with the message 'Missing text'
    - Returns the new Place with the status code 201
    """
    # check if data is sent and is json
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    # check if data has compulsory attributes
    if not all([data, len(data), data.get("user_id")]):
        abort(400, description="Missing user_id")
    if not data.get("text"):
        abort(400, description="Missing text")

    print("400 check passed: ", "{ user_id: ", data.get("user_id"),
          " }", "{ text: ", data.get("text"), " }")
    # check if user_id and place_id is valid
    user = storage.get(User, data.get('user_id'))
    place = storage.get(Place, place_id)
    if not all([user, place]):
        print("caught: 01")
        abort(404)

    # check if user_id and place_id of place match
    if not all([place.user_id == data.get('user_id'),
                place.id == place_id]):
        print("caught: 02")
        abort(404)

    # create new review
    new_review = Review(
        place_id=place_id,
        user_id=data.get('user_id'),
        text=data.get('text')
    )

    # save and return
    new_review.save()
    res = json.dumps(new_review.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json", status=201)


@app_views.route('/reviews/<string:rev_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(rev_id):
    """Updates an Review object: PUT /api/v1/reviews/<review_id>

    - If the review_id is not linked to any Review object, raise a 404 error
    - must use request.get_json from Flask to transform the HTTP body
      +request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400
      +error with the message 'Not a JSON'
    - Updates the Review object with all key-value pairs of the dictionary.
    - Ignores keys: id, user_id, place_id, created_at and updated_at
    - Returns the User object with the status code 200
    """
    # check data is valid json and not empty
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")
    if not any([data, len(data), data.get("text")]):
        abort(400, description="Missing text")

    # get place and assign attributes
    review = storage.get(Review, rev_id)
    if not review:
        abort(404)
    if data.get('text'):
        setattr(review, 'text', data['text'])

    # commit changes to storage
    review.save()
    res = json.dumps(review.to_dict(), indent=2) + '\n'
    return Response(res, mimetype="application/json")
