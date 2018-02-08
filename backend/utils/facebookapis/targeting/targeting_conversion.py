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


def update_conversion_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                              conversion_event_name="ViewContent"):
    try:
        custom_audience = CustomAudience(custom_audience_id)

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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 미 전환 고객
def create_non_conversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
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

# 미 전환 고객
def update_non_conversion_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                    conversion_event_name="ViewContent"):
    try:
        custom_audience = CustomAudience(custom_audience_id)

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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 전환 URL완료 고객
def create_conversion_url_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                              current_url='', next_url=''):
    try:
        ad_account = AdAccount(fbid=account_id)

        rule = {
            "inclusions":{
                "operator":"or",
                "rules":[
                    {
                        "event_sources":[
                            {
                                "type":"pixel",
                                "id":pixel_id
                            }
                        ],
                        "retention_seconds":retention_days * 24 * 60 * 60,
                        "filter":{
                            "operator":"and",
                            "filters":[
                                {
                                    "field":"url",
                                    "operator":"i_contains",
                                    "value":current_url
                                },
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": next_url
                                }
                            ]
                        },
                        "template":"VISITORS_BY_URL"
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

def update_conversion_url_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                              current_url='', next_url=''):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        rule = {
            "inclusions":{
                "operator":"or",
                "rules":[
                    {
                        "event_sources":[
                            {
                                "type":"pixel",
                                "id":pixel_id
                            }
                        ],
                        "retention_seconds":retention_days * 24 * 60 * 60,
                        "filter":{
                            "operator":"and",
                            "filters":[
                                {
                                    "field":"url",
                                    "operator":"i_contains",
                                    "value":current_url
                                },
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": next_url
                                }
                            ]
                        },
                        "template":"VISITORS_BY_URL"
                    }
                ]
            }
        }

        params = {}
        params[CustomAudience.Field.name] = name
        params[CustomAudience.Field.prefill] = prefill
        params[CustomAudience.Field.rule] = rule

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
