from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from utils.facebookapis.graph_api import manage_token

from user.models import User

import json
import logging
import traceback

logger = logging.getLogger(__name__)

class Me(APIView):
    def get(self, request, format=None):
        # username = fb_email = fb_id = language = None
        # picture = "static/images/default_user.jpg"
        response_data = {}

        try:
            # Default Image
            login_session = self.request.session['__user_id__']
            user = User.objects.get(username=login_session)

            data = {}
            data["username"] = user.name
            data["fb_email"] = user.email
            data["fb_id"] = user.username
            data["picture"] = user.picture_url
            data["language"] = user.language

            response_data['success'] = 'YES'
            response_data['data'] = data

        except Exception as e:
            logger.error(e)
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class Signin(APIView):
    def post(self, request, format=None):
        response_data = {}
        try:
            print('Signin POST')
            print(request.data)

            fb_username = request.data.get('fb_username', '')
            fb_id = request.data.get('fb_id', '')
            fb_name = request.data.get('fb_name', '')
            fb_gender = request.data.get('fb_gender', '')
            fb_picture_url = request.data.get('fb_picture_url', '')
            fb_access_token = request.data.get('fb_access_token', '')

            user = User()
            try:
                user = User.objects.get(username=fb_id)
            except Exception as user_exception:
                logger.info("user.models.DoesNotExist")
                user.username = fb_id
                user.created_by = fb_name
                user.updated_by = fb_name
                user.role = '0'

            user.email = fb_username
            user.name = fb_name
            user.gender = fb_gender
            user.picture_url = fb_picture_url
            user.fb_access_token = manage_token.extend_long_token(fb_access_token)

            user.save()

            request.session['__user_id__'] = user.username
            request.session['__username__'] = user.name
            request.session.modified = True
            response_data['success'] = 'YES'
        except Exception as e:
            logger.error(e)
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class Signout(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            request.session['__user_id__'] = None
            request.session['__username__'] = None
            request.session.modified = True
            response_data['success'] = 'YES'
        except KeyError as e:
            logger.error(e)
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
