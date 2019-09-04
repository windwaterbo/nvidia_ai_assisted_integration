from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sys
import json
import argparse
import client_api
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
"""Test annotation assistant server."""

sys.path.append('.')
cors = CORS(app, resources={r"*": {"origins": "*"}})
ip = '10.91.4.191'
port = '5000'
api_version = 'v1'
client = client_api.AIAAClient(ip, port, api_version)


# post /fixpolygon
@app.route('/fixpolygon', methods=['POST'])
@cross_origin()
def fix_polygon():
    request_data = request.get_json()
    image_path = request_data.get('image_path')
    result_prefix = 'Outputs/spleen1_polygonUpdate'
    params = request_data.get('params')
    files = client.fixpolygon(image_path, result_prefix, params)
    with open('Outputs/spleen1_polygonUpdate.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

# post /fixpolygon
@app.route('/mask2polygon', methods=['POST'])
@cross_origin()
def mask2polygon():
    request_data = request.get_json()
    image_path = request_data.get('image_path')
    result_prefix = 'Outputs/liver1_polygonUpdate'
    params = request_data.get('params')
    files = client.mask2polygon(image_path, result_prefix, params)
    with open('Outputs/liver1_polygonUpdate.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


app.run(port=5000)
