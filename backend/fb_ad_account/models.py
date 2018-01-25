from django.db import models

import traceback
import logging

logger = logging.getLogger(__name__)


class FbAdAccount(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    ad_account_id = models.BigIntegerField()
    act_account_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128)
    account_status = models.IntegerField(default=2)
    account_category = models.ForeignKey('account_category.AccountCategory', db_constraint=False)
    pixel_id = models.BigIntegerField()

    def create(self, ad_account_id, act_account_id, name, account_statsus, account_category_id, pixel_id, username = 'TEST'):
        try:
            fb_ad_account = self.objects.get(act_account_id=act_account_id)

            fb_ad_account.created_by = username
            fb_ad_account.updated_by = username
            fb_ad_account.ad_account_id = ad_account_id
            fb_ad_account.act_account_id = act_account_id
            fb_ad_account.name = name
            fb_ad_account.account_status = account_statsus
            fb_ad_account.account_category_id = account_category_id
            fb_ad_account.pixel_id = pixel_id

            fb_ad_account.save()

            return fb_ad_account
        except self.DoesNotExist:
            fb_ad_account = FbAdAccount()

            fb_ad_account.created_by = username
            fb_ad_account.updated_by = username
            fb_ad_account.ad_account_id = ad_account_id
            fb_ad_account.act_account_id = act_account_id
            fb_ad_account.name = name
            fb_ad_account.account_status = account_statsus
            fb_ad_account.account_category_id = account_category_id
            fb_ad_account.pixel_id = pixel_id

            fb_ad_account.save()

            return fb_ad_account
        except Exception as e:
            # print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    def find_by_fb_ad_account_id(self, fb_ad_account_id):
        if fb_ad_account_id == '0':
            return None
        try:
            fb_ad_account = self.objects.get(pk=fb_ad_account_id)

            return fb_ad_account
        except self.DoesNotExist:
            return None
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            # TODO return []
            return None

    def find_by_ad_account_id(self, ad_account_id):
        if ad_account_id == '0':
            return None
        try:
            fb_ad_account = self.objects.get(act_account_id=ad_account_id)

            return fb_ad_account
        except self.DoesNotExist:
            return None
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            # TODO return []
            return None


    class Meta:
        db_table = "fb_ad_accounts"
