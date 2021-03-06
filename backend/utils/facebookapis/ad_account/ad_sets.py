from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adsinsights import AdsInsights as Insights

from django.conf import settings
from facebookads.exceptions import FacebookRequestError

import logging
import traceback

logger = logging.getLogger('mod_pickdata')



def field_list():
    fields = [
        AdSet.Field.account_id,
        AdSet.Field.adset_schedule,
        AdSet.Field.bid_amount,
        AdSet.Field.bid_info,
        AdSet.Field.billing_event,
        AdSet.Field.budget_remaining,
        AdSet.Field.campaign_id,
        AdSet.Field.configured_status,
        AdSet.Field.created_time,
        AdSet.Field.creative_sequence,
        AdSet.Field.daily_budget,
        AdSet.Field.effective_status,
        AdSet.Field.end_time,
        AdSet.Field.id,
        AdSet.Field.is_autobid,
        AdSet.Field.lifetime_budget,
        AdSet.Field.name,
        AdSet.Field.optimization_goal,
        AdSet.Field.pacing_type,
        AdSet.Field.promoted_object,
        AdSet.Field.start_time,
        AdSet.Field.status,
        AdSet.Field.targeting,
        AdSet.Field.updated_time,
        AdSet.Field.attribution_spec,
        AdSet.Field.is_average_price_pacing,
        'campaign{id,name,objective}'
    ]

    return fields

def adset_targeting_field():
    fields = [
        'id',
        'campaign{id,name,objective}',
        'name',
        'targeting'
    ]

    return fields

def get_ad_set(adset_id):
    try:
        adset = AdSet(adset_id)
        adset.remote_read(fields=adset_targeting_field())

        return adset._json
    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def get_my_ad_sets(account_id, limit=25, after=None, fields=field_list()):
    try:
        ad_account = AdAccount(account_id)

        params = default_params()
        params['limit'] = limit
        params['locale'] = 'ko_KR'

        if after != None:
            params['after'] = after

        ad_sets = ad_account.get_ad_sets(fields=fields, params=params)

        return ad_sets

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def remote_get_ad_set_by_account_id(account_id, fields=[]):
    try:
        if fields == []:
            fields = field_list()
            ad_account = AdAccount(account_id)
            ad_sets = ad_account.get_ad_sets(fields=fields,
                                             params={
                                                 'locale': 'ko_KR',
                                                 'limit': 500,
                                             })

        return ad_sets
    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
    raise Exception(msg)


def get_insight_by_ad_set(ad_set_id, params={}):
    try:
        ad_set = AdSet(ad_set_id)
        ad_insights = ad_set.get_insights(fields=insight_fields(), params=params)

        return ad_insights

    except FacebookRequestError as e:
        print(traceback.format_exc())
        logger.error(traceback.format_exc())
        msg = e._error
        status_code = e._error['code']
        message = e._error['message']
        if status_code == 1 and message == 'An unknown error occurred':
            logger.info('Unknown Error, Adset Id:', ad_set_id)
            pass
        elif status_code == 1 and message == 'Please reduce the amount of data you\'re asking for, then retry your request':
            logger.info('Reduce data Error, Adset Id:', ad_set_id)
            pass
        else:
            raise Exception(msg)


def insight_fields():
    fields = [
        'account_id',
        'account_name',
        'action_values',
        'actions',
        'ad_id',
        'ad_name',
        'adset_id',
        'adset_name',
        'buying_type',
        'call_to_action_clicks',
        'campaign_id',
        'campaign_name',
        'canvas_avg_view_percent',
        'canvas_avg_view_time',
        'canvas_component_avg_pct_view',
        'clicks',
        'cost_per_10_sec_video_view',
        'cost_per_action_type',
        'cost_per_estimated_ad_recallers',
        'cost_per_inline_link_click',
        'cost_per_inline_post_engagement',
        'cost_per_outbound_click',
        'cost_per_total_action',
        'cost_per_unique_action_type',
        'cost_per_unique_click',
        'cost_per_unique_inline_link_click',
        'cost_per_unique_outbound_click',
        'cpc',
        'cpm',
        'cpp',
        'ctr',
        'date_start',
        'date_stop',
        'estimated_ad_recall_rate',
        'estimated_ad_recallers',
        'frequency',
        'impressions',
        'inline_link_click_ctr',
        'inline_link_clicks',
        'inline_post_engagement',
        'mobile_app_purchase_roas',
        'objective',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'place_page_name',
        'reach',
        'relevance_score',
        'social_clicks',
        'social_impressions',
        'social_reach',
        'social_spend',
        'spend',
        'total_action_value',
        'total_actions',
        'total_unique_actions',
        'unique_actions',
        'unique_clicks',
        'unique_ctr',
        'unique_inline_link_click_ctr',
        'unique_inline_link_clicks',
        'unique_link_clicks_ctr',
        'unique_outbound_clicks',
        'unique_outbound_clicks_ctr',
        'unique_social_clicks',
        # 'video_3_sec_watched_actions',
        'video_10_sec_watched_actions',
        # 'video_15_sec_watched_actions',
        'video_30_sec_watched_actions',
        'video_avg_percent_watched_actions',
        'video_avg_time_watched_actions',
        'video_p100_watched_actions',
        'video_p25_watched_actions',
        'video_p50_watched_actions',
        'video_p75_watched_actions',
        'video_p95_watched_actions',
        'website_ctr',
        'website_purchase_roas'
    ]

    return fields


def default_params():
    defult_parms = {
        'locale': 'ko_KR'
    }

    return defult_parms
