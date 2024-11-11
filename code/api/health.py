import requests
from http import HTTPStatus
from flask import Blueprint, current_app

from api.utils import jsonify_data, get_key
from api.errors import (
    AuthenticationRequiredError,
    UnexpectedError,
    InternalServerError,
    NotFoundError,
    SSLError
)

health_api = Blueprint('health', __name__)

@health_api.route('/health', methods=['POST'])
def health():
    
    key = get_key()

    if key is None:
        raise AuthenticationRequiredError
    
    return jsonify_data({'status': 'ok'})
