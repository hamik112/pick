from django.db import models

import traceback
import logging

logger = logging.getLogger(__name__)

class NeoAccount(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', db_constraint=False, null=False)
    neo_adv_id = models.IntegerField()
    neo_account_id = models.IntegerField()

    def get_list_by_fb_ad_account_id(self, fb_ad_account_id=0):
        if fb_ad_account_id == 0:
            return []
        try:
            neo_accounts = self.objects.get(fb_ad_account_id=fb_ad_account_id)

            return_data = []

            for neo_account in neo_accounts:
                return_data.append({
                    "neo_adv_id" : neo_account.neo_adv_id,
                    "neo_account_id" : neo_account.neo_account_id,
                    "fb_ad_account_id": neo_account.fb_ad_account_id
                })


            return return_data
        except self.DoesNotExist:
            return []
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            # TODO return []
            return []

    class Meta:
        db_table = "neo_accounts"