#!/usr/bin/python3
"""API Flask App module"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """Close session bu calling close()"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Not found error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host=host, port=port, threaded=True)
