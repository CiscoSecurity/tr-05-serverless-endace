import requests
from http import HTTPStatus
from flask import Blueprint, current_app

from api.utils import jsonify_data
from api.errors import (
    EndaceUnexpectedError,
    EndaceInternalServerError,
    EndaceNotFoundError,
    EndaceSSLError
)

health_api = Blueprint('health', __name__)

# TODO: connect to probe URL and check for valid response.
@health_api.route('/health', methods=['POST'])
def health():
    return jsonify_data({'status': 'ok'})


