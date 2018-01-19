from django.db import models
from fb_ad_account.models import FbAdAccount
from neo_db.models import McCenterAdvertiser, McCenterAccount

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

    def create(self, fb_ad_account_id, neo_adv_id, neo_account_id, username = 'TEST'):
        try:
            neo_account = NeoAccount()

            neo_account.updated_by = username
            neo_account.created_by = username

            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)
            if fb_ad_account == None:
                raise Exception("Not valid fb_ad_account_id.")

            neo_account.fb_ad_account = fb_ad_account
            neo_account.neo_adv_id = neo_adv_id
            neo_account.neo_account_id = neo_account_id

            neo_account.save()

            return neo_account

        except Exception as e:
            # print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    def create_list(self, fb_ad_account_id, neo_adv_ids = [], neo_account_ids = [], username = 'TEST'):
        try:
            before_neo_accounts = self.objects.filter(fb_ad_account_id=fb_ad_account_id)

            before_neo_accounts.delete()

            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)
            if fb_ad_account == None:
                raise Exception("Not valid fb_ad_account_id.")

            create_cnt = 0
            for idx, neo_account_id in enumerate(neo_account_ids):

                neo_account = NeoAccount()
                neo_account.updated_by = username
                neo_account.created_by = username

                neo_account.fb_ad_account = fb_ad_account
                neo_account.neo_adv_id = neo_adv_ids[idx]
                neo_account.neo_account_id = neo_account_ids[idx]

                neo_account.save()
                create_cnt += 1

            return create_cnt

        except Exception as e:
            # print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None


    def get_list_by_fb_ad_account_id(self, fb_ad_account_id=0):
        if fb_ad_account_id == 0:
            return []
        try:
            neo_accounts = self.objects.filter(fb_ad_account_id=fb_ad_account_id)

            adv_ids = [neo_account.neo_adv_id for neo_account in neo_accounts]
            adv_ids = list(set(adv_ids))
            account_ids = [neo_account.neo_account_id for neo_account in neo_accounts]

            neo_advs = McCenterAdvertiser.get_advertisers_by_ids(McCenterAdvertiser, adv_ids)
            neo_accs = McCenterAccount.get_accounts_by_ids(McCenterAccount, account_ids)

            dic_neo_advs = {}
            dic_neo_accs = {}

            for neo_adv in neo_advs:
                print(neo_adv.advertiserid)
                dic_neo_advs[neo_adv.advertiserid] = neo_adv
            for neo_acc in neo_accs:
                dic_neo_accs[neo_acc.centeraccountid] = neo_acc

            return_data = []

            for neo_account in neo_accounts:
                return_data.append({
                    "id" : neo_account.id,
                    "neo_adv_id" : neo_account.neo_adv_id,
                    "neo_adv_name": dic_neo_advs.get(neo_account.neo_adv_id).advertisername,
                    "neo_account_id" : neo_account.neo_account_id,
                    "neo_account_name" : dic_neo_accs.get(neo_account.neo_account_id).accountnickname,
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