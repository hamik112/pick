from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.exceptions import FacebookRequestError

def get_by_ids_target_insights(adset_ids):

    try:
        for adset_id in adset_ids:

            adset = AdSet(adset_id)

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

def get_adset_ids_placement_insights(act_account_id, adset_ids , start_date=None, end_date=None):
    try:
        ad_account = AdAccount(act_account_id)

        fields = [
            AdsInsights.Field.adset_id,
            AdsInsights.Field.impressions,
        ]
        params = {
            'level': 'adset',
            'filtering': [
                {
                    'field': 'adset.id',
                    'operator': 'IN',
                    'value': adset_ids,
                }
            ],
            'breakdowns': [
                AdsInsights.Breakdowns.publisher_platform,
                AdsInsights.Breakdowns.impression_device
            ]

        }

        if start_date != None and end_date != None:
            params['time_range'] = {
                'since': start_date,
                'until': end_date
            }
        else:
            params['date_preset'] = AdsInsights.DatePreset.today
            # TODO DELETE
            params['date_preset'] = AdsInsights.DatePreset.lifetime

        adset_insights = ad_account.get_insights(fields=fields, params=params)

        return adset_insights

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def get_adset_ids_agegender_insights(act_account_id, adset_ids , start_date=None, end_date=None):
    try:
        ad_account = AdAccount(act_account_id)

        fields = [
            AdsInsights.Field.adset_id,
            AdsInsights.Field.impressions,
        ]
        params = {
            'level': 'adset',
            'filtering': [
                {
                    'field': 'adset.id',
                    'operator': 'IN',
                    'value': adset_ids,
                }
            ],
            'breakdowns': [
                AdsInsights.Breakdowns.age,
                AdsInsights.Breakdowns.gender
            ]

        }

        if start_date != None and end_date != None:
            params['time_range'] = {
                'since': start_date,
                'until': end_date
            }
        else:
            params['date_preset'] = AdsInsights.DatePreset.today
            # TODO DELETE
            params['date_preset'] = AdsInsights.DatePreset.lifetime

        adset_insights = ad_account.get_insights(fields=fields, params=params)

        return adset_insights

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def get_adset_id_placement_insights(adset_id):
    try:
        adset = AdSet(adset_id)

        adset_placements_insights = adset.get_insights(
            fields=[

            ],
            params={
                'breakdowns': [
                    AdsInsights.Breakdowns.publisher_platform,
                    AdsInsights.Breakdowns.impression_device
			    ],
            }
        )

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
