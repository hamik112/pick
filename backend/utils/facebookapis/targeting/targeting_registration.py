from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 회원가입 전체 고객
def create_regestration_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                  regestration_event_name="CompleteRegistration"):
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
                                    "value": regestration_event_name
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


# 회원가입 이용시간 상위 고객
def create_regestration_usage_time_top_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 regestration_event_name="CompleteRegistration", input_percent=25):
    try:
        ad_account = AdAccount(fbid=account_id)
        max_percent = 100

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
                        # "retention_seconds": retention_days * 24 * 60 * 60,
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": regestration_event_name
                                }
                            ]
                        }
                    },
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


# 회원가입 미구매 고객
def create_regestration_and_non_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                   regestration_event_name="CompleteRegistration",
                                                   purchase_event_name="Purchase"):
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
                        # "retention_seconds": retention_days * 24 * 60 * 60,
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": regestration_event_name
                                }
                            ]
                        }
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


# 회원가입 전환완료 고객
def create_regestration_and_conversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 regestration_event_name="CompleteRegistration",
                                                 conversion_event_name="ViewContent"):
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
                        # "retention_seconds": retention_days * 24 * 60 * 60,
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": regestration_event_name
                                }
                            ]
                        }
                    },
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


# 회원가입 미전환 고객
def create_regestration_non_conversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 regestration_event_name="CompleteRegistration",
                                                 conversion_event_name="ViewContent"):
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
                        # "retention_seconds": retention_days * 24 * 60 * 60,
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "event",
                                    "operator": "eq",
                                    "value": regestration_event_name
                                }
                            ]
                        }
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
