from django.conf import settings

import facebook

import pprint
import logging
import traceback

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

def extend_long_token(short_access_token):
    try:
        fb_app_id = settings.FACEBOOK_APP_ID
        fb_app_secret = settings.FACEBOOK_APP_SECRET

        graph = facebook.GraphAPI(short_access_token, version='2.10')
        res = graph.extend_access_token(fb_app_id, fb_app_secret)
        return res['access_token']
    except facebook.GraphAPIError as e:
        print(traceback.format_exc())
        logger.error(e.result)
        return ''

def request_debug_token(access_token):
    try:
        args = {'input_token': access_token}

        graph = facebook.GraphAPI(access_token, version='2.10')
        res = graph.request('me', args)
        logger.debug(res.get('data', ''))

        return True
    except facebook.GraphAPIError as e:
        print(traceback.format_exc())
        logger.error(e.result)
        return False
