from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 전환 완료 고객
def create_conversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                              conversion_event_name="ViewContent"):
    try:
        ad_account = AdAccount(fbid=account_id)

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
                                    "field": "event",
                                    "operator": "eq",
                                    "value": conversion_event_name
                                }
                            ]
                        }
                    }
                ]
            }
        }

        params = {}
        params[CustomAudience.Field.name] = name
        params[CustomAudience.Field.prefill] = prefill
        params[CustomAudience.Field.rule] = rule

        audience = ad_account.create_custom_audience(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)



