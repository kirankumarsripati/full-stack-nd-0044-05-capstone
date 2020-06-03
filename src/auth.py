import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-jv5b18wv.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'FSND'


class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    '''
    Attempts to get the header from the request
    Raises an AuthError if no header is present
    Attempt to split bearer and the token
    Raises an AuthError if the header is malformed

    Returns:
    str: the token part of the header

    Precondition:
    Authorization header is available
    It should follow format Bearer xxxxxx
    '''
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)

    # expecting Authorization as Bearer xxxxx
    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization must start with Bearer'
        }, 401)

    elif len(parts) == 1:
        # token is missing
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)

    elif len(parts) > 2:
        # required only 2 parts
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    '''
    Checks if permission is available in payload
    Raises an AuthError if permissions are not included in the payload
    Raises an AuthError if the requested permission string is not in
    the payload permissions array

    Parameters:
    permission (string): permission (i.e. 'post:drink')
    payload (string): decoded jwt payload

    Returns:
    True if matched or throws AuthError
    '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 401)
    return True


def verify_decode_jwt(token):
    '''
    Verifies JWT Token with the Auth0
    it should be an Auth0 token with key id (kid)
    Verify the token using Auth0 /.well-known/jwks.json
    Decode the payload from the token
    Validate the claims

    Parameters:
    token (string): a json web token

    Returns:
    str: decoded payload or throws AuthError
    '''
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    # should be an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if not rsa_key:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find appropriate key'
        }, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer='https://' + AUTH0_DOMAIN + '/'
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired'
        }, 401)

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims, please, check the \
                audience and issuer'
        }, 401)

    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token'
        }, 401)


def requires_auth(permission=''):
    '''
    Checks with the decorator endpoint with the provided permission
    Uses the get_token_auth_header method to get the token
    Uses the verify_decode_jwt method to decode the jwt
    Uses the check_permissions method validate claims
    and check the requested permission

    Parameters:
    permission (string): permission (i.e. 'post:drink')

    Returns:
    func: the decorator which passes the decoded
    payload to the decorated method
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
