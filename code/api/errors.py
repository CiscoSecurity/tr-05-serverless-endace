INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
NOT_FOUND = 'not found'
INTERNAL = 'internal error'
HEALTH_CHECK_ERROR = 'Health check failed'
MISSING_PROBE_FQDN = 'EndaceProbe FQDN is missing'
AUTH_ERROR = 'authorization error'
NO_AUTH_HEADER = 'authorization header is missing'
WRONG_AUTH_TYPE = 'Wrong authorization type'
WRONG_PAYLOAD_STRUCTURE = 'Wrong JWT payload structure'
WRONG_JWT_STRUCTURE = 'Wrong JWT structure'
WRONG_AUDIENCE = 'Wrong configuration-token-audience'
KID_NOT_FOUND = 'kid from JWT header not found in API response'
WRONG_KEY = ('Failed to decode JWT with provided key. '
             'Make sure domain in custom_jwks_host '
             'corresponds to your SecureX instance region.')
JWK_HOST_MISSING = ('jwks_host is missing in JWT payload. Make sure '
                    'custom_jwks_host field is present in module_type')
WRONG_JWKS_HOST = ('Wrong jwks_host in JWT payload. Make sure domain follows '
                   'the visibility.<region>.cisco.com structure')

class CTRBaseError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code,
                'message': self.message}

class UnexpectedError(CTRBaseError):
    def __init__(self, response):
        super().__init__(
            response.reason,
            'An unexpected error occurred trying to connect to the target EndaceProbe.'
        )


class InternalServerError(CTRBaseError):
    def __init__(self):
        super().__init__(
            INTERNAL,
            'An internal Error occurred on the target EndaceProbe.'
        )


class NotFoundError(CTRBaseError):
    def __init__(self):
        super().__init__(
            NOT_FOUND,
            'Cannot connect to EndaceProbe specified in module configuration.'
        )

class SSLError(CTRBaseError):
    def __init__(self, error):
        error = error.args[0].reason.args[0]
        message = getattr(error, 'verify_message', error.args[0]).capitalize()
        super().__init__(
            UNKNOWN,
            f'Unable to verify SSL certificate: {message}'
        )

class WatchdogError(CTRBaseError):
    def __init__(self):
        super().__init__(
            HEALTH_CHECK_ERROR,
            'Invalid Health Check'
        )


class InvalidPayloadReceivedError(CTRBaseError):
    def __init__(self, message):
        super().__init__(
            INVALID_ARGUMENT,
            f'Invalid JSON Payload Received: {message}'
        )
        
class ProbeFQDNError(CTRBaseError):
    def __init__(self):
        super().__init__(
            MISSING_PROBE_FQDN,
            f'Details: {MISSING_PROBE_FQDN}'
        )  
            
class AuthenticationRequiredError(CTRBaseError):
    def __init__(self, code=UNKNOWN):          
        super().__init__(
            code,
            f'Details: {code}'
        )


