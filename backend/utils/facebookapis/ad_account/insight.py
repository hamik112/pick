from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.exceptions import FacebookRequestError

def get_adset_level_yesterday_insights(act_account_id):

    try:
        ad_account = AdAccount(act_account_id)

        params = {
            "date_preset": "yesterday",
            'level': 'adset'
        }

        adset_insights = ad_account.get_insights(
            fields=insight_fields(), params=params
        )

        return adset_insights

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def get_adset_level_select_date_insights(act_account_id, select_date):

    try:
        ad_account = AdAccount(act_account_id)

        params = {
            'level': 'adset',
            "time_increment": 1,
            "time_range": {
                "since": select_date,
                "until": select_date
            }
        }

        adset_insights = ad_account.get_insights(
            fields=insight_fields(), params=params
        )

        return adset_insights

    except FacebookRequestError as e:
        try:
            adset_insights = ad_account.get_insights(
                fields=insight_fields(), params=params
            )

            return adset_insights
        except FacebookRequestError as e:
            try:
                adset_insights = ad_account.get_insights(
                    fields=insight_fields(), params=params
                )

                return adset_insights
            except FacebookRequestError as e:
                try:
                    adset_insights = ad_account.get_insights(
                        fields=insight_fields(), params=params
                    )

                    return adset_insights
                except FacebookRequestError as e:
                    try:
                        adset_insights = ad_account.get_insights(
                            fields=insight_fields(), params=params
                        )

                        return adset_insights
                    except FacebookRequestError as e:
                        print(e)
                        msg = {}
                        msg['request_context'] = e._request_context
                        msg['error'] = e._error
                        raise Exception(msg)

def get_adset_level_select_date_carousel_insights(act_account_id, select_date):

    try:
        ad_account = AdAccount(act_account_id)

        params = {
            'level': 'adset',
            'filtering': [
                {
                    'field': 'action_type',
                    'operator': 'IN',
                    'value': ['link_click']
                }
            ],
            "action_breakdowns":
                [
                    'action_carousel_card_id',
                    'action_carousel_card_name',
                    'action_type'
                ],
            "time_range": {
                "since": select_date,
                "until": select_date
            }
        }

        adset_insights = ad_account.get_insights(
            fields=[
                "date_start", "date_stop", "adset_id", "actions"
            ], params=params
        )

        return adset_insights

    except FacebookRequestError as e:
        try:
            adset_insights = ad_account.get_insights(
                fields=insight_fields(), params=params
            )

            return adset_insights
        except FacebookRequestError as e:
            try:
                adset_insights = ad_account.get_insights(
                    fields=insight_fields(), params=params
                )

                return adset_insights
            except FacebookRequestError as e:
                try:
                    adset_insights = ad_account.get_insights(
                        fields=insight_fields(), params=params
                    )

                    return adset_insights
                except FacebookRequestError as e:
                    try:
                        adset_insights = ad_account.get_insights(
                            fields=insight_fields(), params=params
                        )

                        return adset_insights
                    except FacebookRequestError as e:
                        print(e)
                        msg = {}
                        msg['request_context'] = e._request_context
                        msg['error'] = e._error
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
