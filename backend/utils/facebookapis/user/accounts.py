from facebookads.adobjects.user import User
from facebookads.adobjects.adaccount import AdAccount
from facebookads.exceptions import FacebookRequestError


def default_params():
    defult_parms = {
        'locale': 'ko_KR'
    }

    return defult_parms


def account_fields(key):
    fields = []

    if key == 'default':
        fields = [
            AdAccount.Field.id,
            AdAccount.Field.account_id,
            AdAccount.Field.name,
            AdAccount.Field.account_status,
            AdAccount.Field.funding_source_details,
            AdAccount.Field.funding_source,
        ]

    return fields


def get_my_accounts(fields=account_fields('default')):
    try:
        me = User(fbid='me')
        params = default_params()

        my_accounts = me.get_ad_accounts(fields=fields, params=params)

        return my_accounts

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
