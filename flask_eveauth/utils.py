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
    pass
