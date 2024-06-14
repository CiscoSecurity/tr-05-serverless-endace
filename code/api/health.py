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

# Not much else to do here other than return OK
@health_api.route('/health', methods=['POST'])
def health():
    return jsonify_data({'status': 'ok'})


