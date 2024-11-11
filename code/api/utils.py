import json
from os import cpu_count
from typing import Optional

import jwt
from pprint import *
import requests
from flask import request, current_app, jsonify, g
from json.decoder import JSONDecodeError
from jwt import InvalidSignatureError, InvalidAudienceError, DecodeError
from requests.exceptions import ConnectionError, InvalidURL, HTTPError

from api.errors import *

def get_endaceprobe_fqdn(payload):
    try:
        assert isinstance(payload['endaceprobe_fqdn'], str)
        assert payload['endaceprobe_fqdn'] != ""

    except (KeyError, ValueError, AssertionError, TypeError):
        raise ProbeFQDNError

    current_app.config['endaceprobe_fqdn'] = payload['endaceprobe_fqdn']

def get_auth_token():
    expected_errors = {
        KeyError: NO_AUTH_HEADER,
        AssertionError: WRONG_AUTH_TYPE
    }
    try:
        scheme, token = request.headers['Authorization'].split()
        assert scheme.lower() == 'bearer'
        return token
    except tuple(expected_errors) as error:
        raise AuthenticationRequiredError(expected_errors[error.__class__])

def get_public_key(jwks_host, token):
    expected_errors = (
        ConnectionError,
        InvalidURL,
        JSONDecodeError,
        HTTPError
    )
    try:
        response = requests.get(f"https://{jwks_host}/.well-known/jwks")
        response.raise_for_status()
        jwks = response.json()

        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(
                json.dumps(jwk)
            )
        kid = jwt.get_unverified_header(token)['kid']
        return public_keys.get(kid)

    except expected_errors:
        raise AuthenticationRequiredError(WRONG_JWKS_HOST)


def get_key() -> Optional[str]:
    """
    Get authorization token and validate its signature against the public key
    from /.well-known/jwks endpoint
    """
    expected_errors = {
        KeyError: WRONG_PAYLOAD_STRUCTURE,
        AssertionError: JWK_HOST_MISSING,
        InvalidSignatureError: WRONG_KEY,
        DecodeError: WRONG_JWT_STRUCTURE,
        InvalidAudienceError: WRONG_AUDIENCE,
        TypeError: KID_NOT_FOUND
    }

    token = get_auth_token()
    try:
        jwks_payload = jwt.decode(token, options={'verify_signature': False})
        assert 'jwks_host' in jwks_payload
        jwks_host = jwks_payload.get('jwks_host')
        key = get_public_key(jwks_host, token)
        aud = request.url_root
        payload = jwt.decode(
            token, key=key, algorithms=['RS256'], audience=[aud.rstrip('/')]
        )

        get_endaceprobe_fqdn(payload)
        return payload['key']
    except tuple(expected_errors) as error:
        pprint(error)
        raise AuthenticationRequiredError(expected_errors[error.__class__])


def get_json(schema):
    data = request.get_json(force=True, silent=True, cache=False)

    error = schema.validate(data)

    if error:
        reason = json.dumps(error)
        raise InvalidPayloadReceivedError(message=reason)

    return data


def jsonify_data(data):
    return jsonify({'data': data})


def jsonify_errors(error):
    payload = error.json

    if 'bundle' in g:
        data = g.bundle.json()
        if data:
            payload['data'] = data

    return jsonify(payload)