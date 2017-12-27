from facebookads.adobjects.user import User
from facebookads.adobjects.adaccount import AdAccount

from facebookads.exceptions import FacebookRequestError

def defult_fields():
    default_field = [
        AdAccount.Field.id,
        AdAccount.Field.account_id,
        AdAccount.Field.name,
        AdAccount.Field.account_status,
        AdAccount.Field.funding_source_details,
        AdAccount.Field.funding_source,
    ]

    return default_field


def default_params():
    defult_parms = {
        'locale': 'ko_KR'
    }

    return defult_parms


def get_my_ad_accounts(field = defult_fields()):
    try:
        me = User(fbid='me')

        params = default_params()

        my_accounts = me.get_ad_accounts(fields=field, params=params)

        json_accounts = [my_account._json for my_account in my_accounts ]

        return json_accounts

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)