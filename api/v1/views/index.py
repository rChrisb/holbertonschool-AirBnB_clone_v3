#!/usr/bin/python3
"""return status OK in json format"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def json_status():
    return jsonify({
        "status": "OK"
        })
