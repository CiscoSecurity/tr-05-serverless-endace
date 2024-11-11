from http import HTTPStatus
from requests.exceptions import SSLError

from pytest import fixture
from unittest import mock

from .utils import headers

from tests.unit.mock_for_tests import (
    RESPONSE_OF_ENRICH_WITH_INVALID_OBS, VALID_ENRICH_RESPONSE
)

def routes():
    yield '/refer/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json():
    return [{'type': 'domain'}]


def test_enrich_call_with_invalid_json_failure(
        route, client,  invalid_json
):
    response = client.post(route,  json=invalid_json)

    assert response.status_code == HTTPStatus.OK
    assert response.json == RESPONSE_OF_ENRICH_WITH_INVALID_OBS

def test_enrich_call_success(route,
                             client,
                             valid_json,
                             mock_request,
                             valid_jwt,
                             get_public_key):
    
    mock_request.return_value = get_public_key
    
    response = client.post(route, json=valid_json, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
    assert response.json == VALID_ENRICH_RESPONSE
