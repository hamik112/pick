from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 사이트방문 전체 고객
def create_total_customers(account_id, name, pixel_id, retention_days=30, prefill=True):
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

        audience = ad_account.create_custom_audience(params={
            CustomAudience.Field.name: name,
            CustomAudience.Field.prefill: prefill,
            CustomAudience.Field.rule: rule
        })

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

def update_total_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True):
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

        audience = custom_audience.remote_update(params={
            CustomAudience.Field.name: name,
            CustomAudience.Field.prefill: prefill,
            CustomAudience.Field.rule: rule
        })

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
        input_percent = int(input_percent)
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

def update_usage_time_top_customers(custom_audience_id, name, pixel_id, prefill=True, retention_days=30, input_percent=25):
    try:
        input_percent = int(input_percent)
        custom_audience = CustomAudience(custom_audience_id)

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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


# 사이트방문 & 특정일 동안 미방문 고객
def create_non_visition_customers(account_id, name, pixel_id, retention_days=30, exclusion_retention_days=1, prefill=True):
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
                        # "retention_seconds": 2592000,
                        "retention_seconds": exclusion_retention_days * 24 * 60 * 60,
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
        params[CustomAudience.Field.rule] = rule
        params[CustomAudience.Field.prefill] = prefill

        audience = ad_account.create_custom_audience(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

def update_non_visition_customers(custom_audience_id, name, pixel_id, retention_days=30, exclusion_retention_days=1, prefill=True):
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
                        # "retention_seconds": 2592000,
                        "retention_seconds": exclusion_retention_days * 24 * 60 * 60,
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
        params[CustomAudience.Field.rule] = rule
        params[CustomAudience.Field.prefill] = prefill

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 사이트방문 and 장바구니 고객
def create_visitor_and_addtocart_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                              addtocart_evnet_name="AddToCart"):
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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
                                    "value": addtocart_evnet_name
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

def update_visitor_and_addtocart_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                              addtocart_evnet_name="AddToCart"):
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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
                                    "value": addtocart_evnet_name
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


# 사이트방문 전체고객 and 구매고객
def create_visitor_and_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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

def update_visitor_and_purchase_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                          purchase_event_name="Purchase"):
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 사이트방문 전체고객 and 미구매고객
def create_visitor_and_non_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
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
                        #"retention_seconds": retention_days * 24 * 60 * 60,
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

def update_visitor_and_non_purchase_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                              purchase_event_name="Purchase"):
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
                        #"retention_seconds": retention_days * 24 * 60 * 60,
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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


# 사이트방문 and 전환완료 고객
def create_visitor_and_coversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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

def update_visitor_and_coversion_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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


# 사이트방문 and 미 전환 고객
def create_visitor_and_non_coversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
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

def update_visitor_and_non_coversion_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
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


# 사이트방문 and 회원가입 고객
def create_visitor_and_registration_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                              registration_event_name="CompleteRegistration"):
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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
                                    "value": registration_event_name
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

def update_visitor_and_registration_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                              registration_event_name="CompleteRegistration"):
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
                        # ], "retention_seconds": retention_days * 24 * 60 * 60,
                        ], "retention_seconds": 15552000,
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
                    },
                    {
                        "event_sources": [
                            {"type": "pixel",
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
                                    "value": registration_event_name
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
