from django.db import models

import traceback
import logging

logger = logging.getLogger(__name__)

class AdSet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)

    account_id = models.CharField(max_length=64, null=False)
    account_name = models.CharField(max_length=256)
    campaign_id = models.CharField(max_length=64, null=False)
    campaign_name = models.CharField(max_length=256)
    campaign_objective = models.CharField(max_length=64)
    adset_id = models.CharField(max_length=64, unique=True)
    adset_name = models.CharField(max_length=256)

    daily_budget = models.CharField(max_length=64)
    lifetime_budget = models.CharField(max_length=64)

    age_min = models.CharField(max_length=8)
    age_max = models.CharField(max_length=8)
    gender = models.CharField(max_length=8)
    targeting = models.TextField()

    include_interests = models.TextField(null=True)
    include_behaviors = models.TextField(null=True)
    exclude_interests = models.TextField(null=True)
    exclude_behaviors = models.TextField(null=True)
    custom_audiences = models.TextField(null=True)
    excluded_custom_audiences = models.TextField(null=True)

    def create_or_update(self, adset_id, account_id=None, account_name=None, campaign_id=None, campaign_name=None, campaign_objective=None,
                         adset_name=None, daily_budget=None, lifetime_budget=None, age_min=None, age_max=None,
                         gender=None, targeting=None, include_interests=[], include_behaviors=[], exclude_interests=[],
                         exclude_behaviors=[], custom_audiences=[], excluded_custom_audiences=[]):
        try:
            params = {}
            if account_id != None:
                params['account_id'] = account_id
            if account_name != None:
                params['account_name'] = account_name
            if campaign_id != None:
                params['campaign_id'] = campaign_id
            if campaign_name != None:
                params['campaign_name'] = campaign_name
            if campaign_objective != None:
                params['campaign_objective'] = campaign_objective
            # if adset_id != None:
            #     params['adset_id'] = adset_id
            if adset_name != None:
                params['adset_name'] = adset_name
            if daily_budget != None:
                params['daily_budget'] = daily_budget
            if lifetime_budget != None:
                params['lifetime_budget'] = lifetime_budget
            if age_min != None:
                params['age_min'] = age_min
            if age_max != None:
                params['age_max'] = age_max
            if gender != None:
                params['gender'] = gender
            if targeting != None:
                params['targeting'] = targeting
            if include_interests != None:
                params['include_interests'] = include_interests
            if include_behaviors != None:
                params['include_behaviors'] = include_behaviors
            if exclude_interests != None:
                params['exclude_interests'] = exclude_interests
            if include_behaviors != None:
                params['exclude_behaviors'] = exclude_behaviors
            if custom_audiences != None:
                params['custom_audiences'] = custom_audiences
            if excluded_custom_audiences != None:
                params['excluded_custom_audiences'] = excluded_custom_audiences

            obj, created = AdSet.objects.update_or_create(
                adset_id=adset_id, defaults=params
            )

            return obj
        except Exception as e:
            # print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    def get_adsets_for_ids(self, adset_ids):
        try:
            adsets = AdSet.objects.filter(adset_id__in=adset_ids)

            return adsets
        except Exception as e:
            # print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    class Meta:
        db_table = "ad_sets"
