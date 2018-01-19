from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience

from facebookads.exceptions import FacebookRequestError

def get_custom_audiences(account_id):
    try:
        ad_account = AdAccount(account_id)

        custom_audiences = ad_account.get_custom_audiences(fields=[
            CustomAudience.Field.id,
            CustomAudience.Field.name,
            CustomAudience.Field.account_id,
            CustomAudience.Field.approximate_count,
            CustomAudience.Field.delivery_status,
            CustomAudience.Field.operation_status,
            CustomAudience.Field.pixel_id,
            CustomAudience.Field.time_created,
            CustomAudience.Field.time_updated
        ])

        return_data = [ custom_audience._json for custom_audience  in custom_audiences ]

        return return_data

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

def get_dic_custom_audiences(account_id):
    try:
        ad_account = AdAccount(account_id)

        custom_audiences = ad_account.get_custom_audiences(fields=[
            CustomAudience.Field.id,
            CustomAudience.Field.name,
            CustomAudience.Field.account_id,
            CustomAudience.Field.approximate_count,
            CustomAudience.Field.delivery_status,
            CustomAudience.Field.operation_status,
            CustomAudience.Field.pixel_id,
            CustomAudience.Field.time_created,
            CustomAudience.Field.time_updated
        ], params={
            'locale': 'ko_KR'
        })

        return_data = { custom_audience.get('id') : custom_audience._json for custom_audience  in custom_audiences }

        return return_data

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)