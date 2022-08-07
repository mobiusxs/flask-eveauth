from flask import request

from .models import User

anonymous_session = User(
    expires_in=-1,
    token_type='anonymous',
    refresh_token='',
    access_token='',
    name='Anonymous User',
    character_id=1
)


def get_current_user():
    session_id = request.cookies.get('eveauth_session')
    if session_id:
        user = User().get(session_id)
        if user:
            return user
    return anonymous_session
