from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 구매고객 전체
def create_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                              purchase_event_name="Purchase"):
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
                                    "value": purchase_event_name
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


# 특정 구매횟수 이상 구매 고객
def create_more_than_x_timtes_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 purchase_evnet_name="Purchase", purchase_cnt=5):
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
                                    "value": purchase_evnet_name
                                }
                            ]
                        },

                        "aggregation": {
                            "type": "count",
                            "method": "absolute",
                            "operator": ">=",
                            "value": purchase_cnt
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


# 특정 구매금액 이상 구매 고객
def create_more_than_x_amount_purchjase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                  purchase_evnet_name="Purchase", minimum_val=5000):
    try:

        ad_account = AdAccount(fbid=account_id)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources":
                            [
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
                                    "value": purchase_evnet_name
                                }
                            ]
                        },
                        "aggregation": {
                            "type": "min",
                            "method": "absolute",
                            "operator": ">=",
                            "field": "value",
                            "value": minimum_val
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
