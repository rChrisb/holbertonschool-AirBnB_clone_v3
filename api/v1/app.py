#!/usr/bin/python3
"""Flask application running on 0.0.0.0:5000"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_handle(app):
    storage.close()


@app.errorhandler(404)
def notfound(app):
    return jsonify({
        "error": "Not found"
        }), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, threaded=True)
