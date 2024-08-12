#!/usr/bin/python3
"""Creates and manages our app for version 1 api"""

from api.v1.views import app_views
from flask import Flask, g, json, Response
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

cors_config = {
    "origins": ["*"]
}

CORS(app, resources={r"/api/v1/*": cors_config})


@app.teardown_appcontext
def teardown_storage(exception):
    """Tears down the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Handles 404 errors in app to return JSON"""
    res = json.dumps({"error": "Not found"}, indent=2) + '\n'
    return Response(res, mimetype="application/json", status=404)


@app.errorhandler(400)
def wrong_data(e):
    """Handles all wrong data related errors"""
    res = json.dumps({"error": e.description}, indent=2) + '\n'
    return Response(res, mimetype="application/json", status=400)


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST') or "0.0.0.0",
        port=getenv('HBNB_API_PORT') or 5000,
        threaded=True
    )
