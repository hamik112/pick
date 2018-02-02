from django.http import HttpResponse

from utils.facebookapis.graph_api import manage_token

from user.models import User

import json
import traceback
import logging

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

logger = logging.getLogger(__name__)

class LoginFilter(MiddlewareMixin):
    def process_request(self, request):
        response_data = {}

        if request.path == '/users/signin':
            # 로그인 시 필터 제외
            pass
        elif request.path == '/users/signin':
            # 로그아웃 시 필터 제외
            pass
        # else:
        #     # DEBUG 개발용
        #     pass
        elif request.path == '/':
            # 로그인 페이지 필터 제외
            pass
        else:
            # 그 외 모든 요청시 로그인 체크
            try:
                login_session = request.session['__user_id__']
                logger.info('session :: ' + str(request.session['__user_id__']))
                user = User.objects.get(username=login_session)
                if manage_token.request_debug_token(user.fb_access_token):
                    pass
                else:
                    raise Exception('Not Logged In')
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())

                response_data['success'] = 'NO'
                response_data['code'] = '999'
                response_data['msg'] = 'Not Logged In'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
