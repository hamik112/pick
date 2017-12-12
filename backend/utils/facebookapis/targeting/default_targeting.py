from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


def create_total_users(account_id, name='', retention_days=15, pixel_id=''):
    try:
        ad_account = AdAccount(fbid=account_id)
        audience = ad_account.create_custom_audience(params={
            CustomAudience.Field.name: name,
            CustomAudience.Field.subtype : CustomAudience.Subtype.website,
            CustomAudience.Field.retention_days: retention_days,
            CustomAudience.Field.pixel_id: pixel_id
        })

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def create_usage_time_top_customers (account_id, name='', retention_days=15, pixel_id='', percent=0):
    try:
        pass

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def create_non_visition_customers(account_id, name='', retention_days=15, pixel_id=''):
    try:
        pass

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
