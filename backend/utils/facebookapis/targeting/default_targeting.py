from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 사이트방문 전체 고객
def create_total_users(account_id, name, pixel_id, retention_days=30, prefill=True):
    try:
        ad_account = AdAccount(fbid=account_id)
        audience = ad_account.create_custom_audience(params={
            CustomAudience.Field.name: name,
            CustomAudience.Field.subtype: CustomAudience.Subtype.website,
            CustomAudience.Field.pixel_id: pixel_id,
            CustomAudience.Field.prefill: prefill,
            CustomAudience.Field.retention_days: retention_days
        })
        # "rule": "{\"and\":[{\"url\":{\"i_contains\":\"\"}}]}"

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


# 사이트방문 이용 시간 상위 고객
# input_percent = [25, 10, 5]
def create_usage_time_top_customers(account_id, name, pixel_id, prefill=True, retention_days=30, input_percent=25):
    try:
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
                                "from": max_percent - input_percent,
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
        params[CustomAudience.Field.rule] = rule

        audience = ad_account.create_custom_audience(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


# 사이트방문 특정일 동안 미방문 고객
def create_non_visition_customers(account_id, name, pixel_id, retention_days=30, prefill=True):
    try:
        ad_account = AdAccount(fbid=account_id)

        rule = {
            "inclusions": {
                "operator": "and",
                "rules": [
                    {
                        "event_sources": [
                            {
                                "type": "pixel",
                                "id": pixel_id
                            }
                        ],
                        "retention_seconds": 15552000,
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
                        "template": "ALL_VISITORS"
                    }
                ]
            },

            "exclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [
                            {
                                "type": "pixel",
                                "id": pixel_id
                            }
                        ],
                        # "retention_seconds": 2592000,
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
                        "template": "ALL_VISITORS"
                    }
                ]
            }
        }

        params = {}
        params[CustomAudience.Field.name] = name
        params[CustomAudience.Field.rule] = str(rule)
        params[CustomAudience.Field.prefill] = prefill

        audience = ad_account.create_custom_audience(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
