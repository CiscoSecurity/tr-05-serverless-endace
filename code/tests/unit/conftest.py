from unittest.mock import MagicMock, patch
from api.errors import *
from pytest import fixture
import jwt
from app import app
from tests.unit.mock_for_tests import (
    PRIVATE_KEY, EXPECTED_RESPONSE_OF_JWKS_ENDPOINT,
    RESPONSE_OF_JWKS_ENDPOINT_WITH_WRONG_KEY
)

@fixture(scope='session')
def client():
    app.rsa_private_key = PRIVATE_KEY
    
    app.testing = True
   
    with app.test_client() as client:
        yield client

@fixture(scope='function')
def mock_request():
    with patch('requests.get') as mock_request:
        yield mock_request

@fixture(scope='session')
def valid_jwt(client):
    def _make_jwt(
            key='test',
            jwks_host='visibility.amp.cisco.com',
            aud='http://localhost',
            kid='02B1174234C29F8EFB69911438F597FF3FFEE6B7',
            wrong_structure=False,
            wrong_jwks_host=False,
            missing_endaceprobe_fqdn=False
    ):
        payload = {
            'key': key,
            'jwks_host': jwks_host,
            'aud': aud,
            'endaceprobe_fqdn': 'someprobe.endace.com'
        }

        if wrong_jwks_host:
            payload.pop('jwks_host')

        if wrong_structure:
            payload.pop('key')
            
        if missing_endaceprobe_fqdn:
            payload.pop('endaceprobe_fqdn')          

        return jwt.encode(
            payload, client.application.rsa_private_key, algorithm='RS256',
            headers={
                'kid': kid
            }
        )

    return _make_jwt

@fixture(scope='module')
def valid_json():
    return [{'type': 'ip', 'value': '185.53.179.29'}]

@fixture(scope='session')
def get_public_key():
    mock_response = MagicMock()
    payload = EXPECTED_RESPONSE_OF_JWKS_ENDPOINT
    mock_response.json = lambda: payload
    return mock_response

@fixture(scope='session')
def get_wrong_public_key():
    mock_response = MagicMock()
    payload = RESPONSE_OF_JWKS_ENDPOINT_WITH_WRONG_KEY
    mock_response.json = lambda: payload
    return mock_response

   