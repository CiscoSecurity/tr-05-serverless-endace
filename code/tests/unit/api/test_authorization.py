from http import HTTPStatus

from api.errors import *
from api.utils import get_public_key
from .utils import headers

from pytest import fixture
from requests.exceptions import ConnectionError, InvalidURL

def routes():
    yield '/health'
    yield '/refer/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def authorization_errors_expected_payload(route):
    def _make_payload_message(message):
        payload = {
            'code': message,
            'message': f'Details: {message}',
            'type': 'fatal'
        }
        return payload

    return _make_payload_message


def test_call_without_authorization_header_failure(
        route, client, valid_json,
        authorization_errors_expected_payload
):
    response = client.post(route, json=valid_json)

    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        NO_AUTH_HEADER
    )


def test_call_with_wrong_auth_type(
        route, client, valid_json, valid_jwt,
        authorization_errors_expected_payload
):
    response = client.post(
        route, json=valid_json,
        headers={'Authorization': 'bla bla'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        WRONG_AUTH_TYPE
    )


def test_call_with_wrong_jwks_host(
        mock_request, route, client, valid_json, valid_jwt,
        authorization_errors_expected_payload, get_public_key
):
    for error in (ConnectionError, InvalidURL):
        mock_request.side_effect = error()

        response = client.post(
            route, json=valid_json, headers=headers(valid_jwt())
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json == authorization_errors_expected_payload(
            WRONG_JWKS_HOST
        )


def test_call_with_wrong_jwt_payload_structure(
        mock_request, route, client, valid_json, valid_jwt,
        authorization_errors_expected_payload, get_public_key
):
    mock_request.return_value = get_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers(valid_jwt(wrong_structure=True))
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        WRONG_PAYLOAD_STRUCTURE
    )


def test_call_with_missing_jwks_host(
        mock_request, route, client, valid_json, valid_jwt,
        get_public_key, authorization_errors_expected_payload
):
    mock_request.return_value = get_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers(valid_jwt(wrong_jwks_host=True))
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        JWK_HOST_MISSING
    )


def test_call_with_wrong_key(
        mock_request, route, client, valid_json, valid_jwt,
        get_wrong_public_key, authorization_errors_expected_payload
):
    mock_request.return_value = get_wrong_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers(valid_jwt())
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        WRONG_KEY
    )


def test_call_with_wrong_jwt_structure(
        mock_request, route, client, valid_json,
        get_public_key, authorization_errors_expected_payload
):
    mock_request.return_value = get_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers('valid_jwt()')
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        WRONG_JWT_STRUCTURE
    )


def test_call_with_wrong_audience(
        mock_request, route, client, valid_json, valid_jwt,
        get_public_key, authorization_errors_expected_payload
):
    mock_request.return_value = get_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers(valid_jwt(aud='wrong_audience'))
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        WRONG_AUDIENCE
    )


def test_call_with_wrong_kid(
        mock_request, route, client, valid_json, valid_jwt,
        get_public_key, authorization_errors_expected_payload
):
    mock_request.return_value = get_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers(valid_jwt(kid='wrong_kid'))
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        KID_NOT_FOUND
    )

def test_call_with_no_endaceprobe_fqdn(
        mock_request, route, client, valid_json, valid_jwt,
        get_public_key, authorization_errors_expected_payload
):
    mock_request.return_value = get_public_key

    response = client.post(
        route, json=valid_json,
        headers=headers(valid_jwt(missing_endaceprobe_fqdn=True))
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_errors_expected_payload(
        MISSING_PROBE_FQDN
    )       
    
