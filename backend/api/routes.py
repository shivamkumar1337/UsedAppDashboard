from flask import Blueprint, jsonify
from . import db_utils
from flask_cors import cross_origin

api_bp = Blueprint('api', __name__)

@api_bp.route('/data', methods=['GET'])
# @cross_origin()  # Apply CORS to this route
def get_data():
    data = db_utils.fetch_data()
    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Unable to fetch data"}), 500

@app_bi.route('/app_usage', methods=['GET'])
def app_usage():
    records = db_utils.fetch_app_usage()
    return jsonify(records)
