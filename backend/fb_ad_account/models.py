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
    act_account_id = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    account_status = models.IntegerField(default=2)
    account_category = models.ForeignKey('account_category.AccountCategory', db_constraint=False, null=False)

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

    def create_fb_ad_account(self, ad_account_id, name, account_status, account_category):
        try:
            fb_ad_account = FbAdAccount()

            fb_ad_account.ad_account_id = ad_account_id
            fb_ad_account.act_account_id = 'act_' + str(ad_account_id)
            fb_ad_account.name = name
            fb_ad_account.account_status = account_status
            fb_ad_account.account_category = account_category

            fb_ad_account.save()

        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    class Meta:
        db_table = "fb_ad_accounts"
