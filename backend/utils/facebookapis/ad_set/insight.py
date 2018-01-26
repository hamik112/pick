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

def get_adset_ids_placement_insights(act_account_id, adset_ids):
    try:
        print('get_adset_ids_placement_insights')
        print('act_account_id : ', act_account_id)
        print('adset_ids : ', adset_ids)

        ad_account = AdAccount(act_account_id)

        fields = [
            AdsInsights.Field.adset_id,
            AdsInsights.Field.impressions,
        ]
        params = {
            'date_preset' : AdsInsights.DatePreset.lifetime,
            'level': 'account',
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

        adset_insights = ad_account.get_insights(fields=fields, params=params)
        print(len(adset_insights))

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
