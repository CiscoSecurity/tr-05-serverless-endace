from api.errors import INVALID_ARGUMENT
from pytest import fixture

from app import app


@fixture(scope='session')
def client():
    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='module')
def invalid_json_expected_payload(route, client):
    if route.endswith('/refer/observables'):
        return {'errors': [
            {'code': INVALID_ARGUMENT,
             'message': "Invalid JSON payload received. "
                        "{0: {'value': ['Missing data for required field.']}}",
             'type': 'fatal'}
        ]}

    else:
        return {'data': {}}


@fixture(scope='module')
def success_expected_payload(route, client):
    if route.endswith('/refer/observables'):
        return {
            "data": [
                {
                    "categories": [
                        "Search",
                        "Endace"
                    ],
                    "description": "Generate a Pivot-to-Vision URL from this IP address",
                    "id": "ref-shodan-search-ip-185.53.179.29",
                    "title": "Create link for this IP",
                    "url": "localhost/vision2/v1/pivotintovision/?datasources=tag%3Arotation-file%26title=Pivot%20from%20XDR%26ip=185.53.179.29%26tools=conversations_by_ipaddress"
                }
            ]
        }

    else:
        return {'data': {}}
