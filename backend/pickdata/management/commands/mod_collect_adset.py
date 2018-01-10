__author__ = 'parkjiminy'
from ad_set.models import AdSet
from utils.facebookapis import api_init
from utils.facebookapis.ad_account import ad_accounts

import logging
import traceback
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

logger = logging.getLogger('mod_pickdata')

'''
ex) python manage.py mod_collect_adset --settings=pickdata.settings.dev
'''


class Command(BaseCommand):
    def add_arguments(self, parser):
        self.stdout.write("--- collect collect adset module start ---")

    def handle(self, *args, **options):
        self.stdout.write("--- collect collect adset module handle ---")
        try:
            api_init.api_init_by_system_user()

            my_accounts = ad_accounts.get_my_ad_accounts()
            # my_accounts = [account._json for account in my_accounts]

            # SAMPLE
            # my_accounts = [
            # 	{
            # 		"id": 'act_894360037304328',
            # 		'name': "KB국민카드(엠포스)"
            # 	}
            # ]

            for my_account in my_accounts:
                account_id = my_account.get('id')
                account_name = my_account.get('name')

                ad_sets = ad_accounts.get_my_ad_sets(account_id)

                for ad_set in ad_sets:
                    ad_set = ad_set._json
                    campaign_id = ad_set.get('campaign').get('id')
                    campaign_name = ad_set.get('campaign').get('name')
                    campaign_objective = ad_set.get('campaign').get('objective')
                    adset_id = ad_set.get('id')
                    adset_name = ad_set.get('name')
                    lifetime_budget = ad_set.get('lifetime_budget')
                    daily_budget = ad_set.get('daily_budget')
                    targeting = ad_set.get('targeting')

                    include_interests = []
                    include_behaviors = []
                    exclude_interests = []
                    exclude_behaviors = []

                    if targeting != None:
                        flexible_specs = targeting.get('flexible_spec', None)
                        exclusions = targeting.get('exclusions', None)
                        custom_audiences = targeting.get('custom_audiences', [])
                        excluded_custom_audiences = targeting.get('excluded_custom_audiences', [])

                        if flexible_specs != None:
                            # print(flexible_specs)
                            for flexible_spec in flexible_specs:
                                interests = flexible_spec.get('interests', None)
                                behaviors = flexible_spec.get('behaviors', None)
                                if interests != None:
                                    # print("interests : ", interests)
                                    include_interests = include_interests + interests
                                if behaviors != None:
                                    # print("behaviors : ", behaviors)
                                    include_behaviors = include_behaviors + behaviors

                        if exclusions != None:
                            interests = exclusions.get('interests', None)
                            behaviors = exclusions.get('behaviors', None)
                            if interests != None:
                                exclude_interests = interests
                            if behaviors != None:
                                exclude_behaviors = behaviors

                        age_min = targeting.get('age_min', 0)
                        age_max = targeting.get('age_max', 0)
                        gender = targeting.get('gender', [0])

                        create_adset = AdSet.create_or_update(AdSet, adset_id, account_id=account_id,
                                                              account_name=account_name,
                                                              campaign_id=campaign_id, campaign_name=campaign_name,
                                                              campaign_objective=campaign_objective,
                                                              adset_name=adset_name,
                                                              lifetime_budget=lifetime_budget,
                                                              daily_budget=daily_budget,
                                                              targeting=targeting, age_min=age_min, age_max=age_max,
                                                              gender=gender, include_interests=include_interests,
                                                              include_behaviors=include_behaviors,
                                                              exclude_interests=exclude_interests,
                                                              exclude_behaviors=exclude_behaviors,
                                                              custom_audiences=custom_audiences,
                                                              excluded_custom_audiences=excluded_custom_audiences)
                        time.sleep(1)

            logger.info("collect adset module complete")
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("collect adset fail")
