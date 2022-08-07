from base64 import b64decode
from base64 import urlsafe_b64encode
from json import loads
from secrets import token_urlsafe
from urllib.parse import urlencode

from flask import abort
from flask import Blueprint
from flask import current_app
from flask import make_response
from flask import redirect
from flask import request
from flask import url_for
from requests import post

from .models import User

CLIENT_ID = 'd513b498c32048179f0b32c011d03f30'
SECRET_KEY = '4owHmzDSg8WTPYHHkmGuLAGpYHQUAjyc1IhXI5Dy'
CALLBACK_URL = 'http://localhost/auth/callback'
SCOPE = ''
STATE = 'ABC123'

STATE_COOKIE_NAME = 'eveauth_state'
SESSION_COOKIE_NAME = 'eveauth_session'
LOGIN_REDIRECT_URL = 'private.index'
LOGOUT_REDIRECT_URL = 'public.index'


def authorize():
    state = token_urlsafe(64)
    data = {
        'response_type': 'code',
        'redirect_uri': CALLBACK_URL,
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'state': state
    }
    location = f'https://login.eveonline.com/v2/oauth/authorize/?{urlencode(data)}'
    response = make_response(redirect(location=location, code=302))
    response.set_cookie(STATE_COOKIE_NAME, state)
    return response


def callback():
    validate_request_state()
    jwt = request_jwt()
    name, character_id = parse_access_token(jwt['access_token'])
    user = User(
        expires_in=jwt['expires_in'],
        token_type=jwt['token_type'],
        refresh_token=jwt['refresh_token'],
        access_token=jwt['access_token'],
        name=name,
        character_id=character_id,
    )
    user.save()
    response = make_response(redirect(url_for(LOGIN_REDIRECT_URL)))
    response.set_cookie(STATE_COOKIE_NAME, '', expires=0)
    response.set_cookie(SESSION_COOKIE_NAME, user.id)
    return response


def validate_request_state():
    returned_state = request.args.get('state')
    sent_state = request.cookies.get(STATE_COOKIE_NAME)
    if returned_state != sent_state:
        abort(400)


def request_jwt():
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }
    auth_string = f"{CLIENT_ID}:{SECRET_KEY}".encode('utf-8')
    encoded_auth_string = urlsafe_b64encode(auth_string).decode()
    headers = {
        'Authorization': f'Basic {encoded_auth_string}'
    }
    sso_response = post(url='https://login.eveonline.com/v2/oauth/token', data=data, headers=headers)
    sso_response.raise_for_status()
    return sso_response.json()


def parse_access_token(access_token):
    """
        payload = {
            'jti': '0d0193ac-f1ee-4de5-bb66-c8f5f1c3c5f7',
            'kid': 'JWT-Signature-Key',
            'sub': 'CHARACTER:EVE:94268459',
            'azp': 'd513b498c32048179f0b32c011d03f30',
            'tenant': 'tranquility',
            'tier': 'live',
            'region': 'world',
            'aud': 'EVE Online',
            'name': 'Kim Peek',
            'owner': '7N2R8Mg9N99DTwQntwQouWRrRik=',
            'exp': 1659857915,
            'iat': 1659856715,
            'iss': 'login.eveonline.com'
        }
    """

    header, payload, signature = access_token.split('.')
    payload = b64decode(payload + '==')
    payload = loads(payload)
    character_name = payload['name']
    character_id = payload['sub'].split(':')[2]
    return character_name, character_id


def logout():
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        user = User().get(session_id)
        if user:
            user.delete()
    response = make_response(redirect(url_for(LOGOUT_REDIRECT_URL)))
    response.set_cookie(STATE_COOKIE_NAME, '', expires=0)
    response.set_cookie(SESSION_COOKIE_NAME, '', expires=0)
    return response


routes = Blueprint('auth', __name__, url_prefix='/auth')
routes.add_url_rule(rule='/authorize', view_func=authorize, endpoint='authorize', methods=['GET'])
routes.add_url_rule(rule='/callback', view_func=callback, endpoint='callback', methods=['GET'])
routes.add_url_rule(rule='/logout', view_func=logout, endpoint='logout', methods=['GET'])
