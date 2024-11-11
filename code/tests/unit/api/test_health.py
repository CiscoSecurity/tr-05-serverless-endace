from http import HTTPStatus
from requests.exceptions import SSLError
from .utils import headers

from pytest import fixture
from unittest import mock

def routes():
    yield '/health'

@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param

@fixture(scope='function')
def endace_request():
    with mock.patch('requests.get') as mock_request:
        yield mock_request

def test_health_call_success(
        mock_request, route, client, valid_json, valid_jwt, get_public_key
        ):
    
    mock_request.return_value = get_public_key
    
    response = client.post(route, json=valid_json,
        headers=headers(valid_jwt()))
    
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'data': {'status': 'ok'}}
