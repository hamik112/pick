from facebookads.exceptions import FacebookRequestError
# from django.conf import settings

from facebookads import FacebookAdsApi
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.adobjects.adaccount import AdAccount

SYSTEM_USER_TOKEN = 'EAAUsxsN1snQBAHss8zEYNWpegIrZCLiOzZASUoAAyR177teuCatcjFdTRHSZBKrsRz06tAGVDpmra3UEwjaRwxxg0QCJ7qDyOpGzt5G4z7wTnDDctQZCFSlNcLf5222gRJsKkEscRgv6tkIggAiV8zY9jmhQSpAWYkMWmEqSUwZDZD'
FACEBOOK_APP_ID = 1456607077970548
FACEBOOK_APP_SECRET = 'e74075b09b2854a21a32c79cdad67c60'

try:
    FacebookAdsApi.init(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, SYSTEM_USER_TOKEN)

    account_id = 'act_894360037304328'
    name = 'test_usage_time_top_customer'
    pixel_id = '731124753680105'
    retention_days = 30
    prefill = True
    input_percent = 25

    ad_account = AdAccount(fbid=account_id)

    max_percent = 100
    rule = {
        "inclusions": {
            "operator": "or",
            "rules": [
                {
                    "event_sources": [
                        {
                            "type": "pixel",
                            "id": pixel_id
                        }
                    ],
                    "retention_seconds": retention_days * 24 * 60 * 60,
                    "filter": {
                        "operator": "and",
                        "filters": [
                            {
                                "field": "url",
                                "operator": "i_contains",
                                "value": ""
                            }
                        ]
                    },
                    "template": "TOP_TIME_SPENDERS",
                    "aggregation": {
                        "type": "time_spent",
                        "method": "percentile",
                        "operator": "in_range",
                        "value": {
                            "from": max_percent-input_percent,
                            "to": max_percent
                        }
                    }
                }
            ]
        }
    }

    params = {}

    params[CustomAudience.Field.name] = name
    params[CustomAudience.Field.prefill] = prefill
    # str(rule) 사용하면 정상적으로 타겟 생성이 안됨.
    params[CustomAudience.Field.rule] = rule

    audience = ad_account.create_custom_audience(params=params)

    print(audience)

except FacebookRequestError as e:
    print(e)
    msg = {}
    msg['request_context'] = e._request_context
    msg['error'] = e._error
    raise Exception(msg)