from django.conf import settings

from facebookads import FacebookAdsApi
from facebookads.exceptions import FacebookRequestError

facebook_app_id = settings.FACEBOOK_APP_ID
facebook_app_secret = settings.FACEBOOK_APP_SECRET

def api_init(access_token):
    try:
        access_token = access_token

        return FacebookAdsApi.init(facebook_app_id, facebook_app_secret, access_token)

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def api_init_by_system_user():
    try:
        system_user = settings.SYSTEM_USER_TOKEN

        return FacebookAdsApi.init(facebook_app_id, facebook_app_secret, system_user)

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

def api_init_session(request):
    try:
        access_token = find_access_token(request)
        api_init(access_token)
        return access_token
    except Exception as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

def find_access_token(request):
    from user.models import User
    try:
        if '__user_id__' in request.session:
            username = request.session['__user_id__']
        else:
            username = request.session['__user_id__']

        if username == 0:
            raise Exception('Not Exist User.')

        user = User.find_by_username(User, username)
        return user.fb_access_token
    except Exception as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
