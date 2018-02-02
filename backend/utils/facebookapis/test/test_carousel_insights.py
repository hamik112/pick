from facebookads.exceptions import FacebookRequestError
# from django.conf import settings

from facebookads import FacebookAdsApi
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet

SYSTEM_USER_TOKEN = 'EAAUsxsN1snQBAHss8zEYNWpegIrZCLiOzZASUoAAyR177teuCatcjFdTRHSZBKrsRz06tAGVDpmra3UEwjaRwxxg0QCJ7qDyOpGzt5G4z7wTnDDctQZCFSlNcLf5222gRJsKkEscRgv6tkIggAiV8zY9jmhQSpAWYkMWmEqSUwZDZD'
FACEBOOK_APP_ID = 1456607077970548
FACEBOOK_APP_SECRET = 'e74075b09b2854a21a32c79cdad67c60'

try:
    FacebookAdsApi.init(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, SYSTEM_USER_TOKEN)

    account_id = 'act_349408409'

    ad_account = AdAccount(fbid=account_id)

    # adset = AdSet(6066267994652)

    params = {
        'level': 'adset',
        "action_breakdowns": ['action_carousel_card_id', 'action_carousel_card_name', 'action_type'],
        'filtering': [
            {
                'field': 'action_type',
                'operator': 'IN',
                'value': ['link_click'],
            }
        ],
        "time_range": {
            "since": "2017-02-01",
            "until": "2017-02-01"
        }
    }

    fields = [
        "date_start",
        "date_stop",
        "adset_id",
        "actions"
    ]

    adset_insights = ad_account.get_insights(params=params, fields=fields)
    print(adset_insights)

except FacebookRequestError as e:
    print(e)
    msg = {}
    msg['request_context'] = e._request_context
    msg['error'] = e._error
    raise Exception(msg)
