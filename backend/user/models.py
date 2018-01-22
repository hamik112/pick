from django.db import models

import traceback
import logging

logger = logging.getLogger(__name__)

class User(models.Model):
    LANGUAGE_KOREAN = 'ko'
    LANGUAGE_ENGLISH = 'en'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    username = models.CharField(max_length=64, unique=True)
    password_digest = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    fb_access_token = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=32)
    language = models.CharField(max_length=128, default=LANGUAGE_KOREAN)
    login_id = models.CharField(max_length=128, blank=True, null=True, default=None)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=16, null=True, default=None)
    picture_url = models.CharField(max_length=255, blank=True, default='')

    def find_by_username(self, username):
        if username == '0':
            return None
        try:
            user = self.objects.get(username=username)
            return user
        except self.DoesNotExist:
            return None
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            # TODO return []
            return None

    class Meta:
        db_table = "users"
