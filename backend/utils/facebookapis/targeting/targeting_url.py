from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# URL포함 전체 방문자
def create_url_total_visitor_customers(account_id, name, pixel_id, retention_days=30, prefill=True, contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                                }, {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 방문자 & 이용시간 상위 고객
def create_usage_time_top_customers(account_id, name, pixel_id, prefill=True, retention_days=30, input_percent=25, contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
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


# URL포함 & 특정일 동안 미방문 고객
def create_non_visition_customers(account_id, name, pixel_id, prefill=True, retention_days=30, contain_list=[]):
    try:

        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 and 장바구니 고객

def create_url_and_addtocart_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 addtocart_evnet_name="AddToCart", contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        ], "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 & 구매고객
def create_url_and_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                purchase_event_name="Purchase", contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        ], "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 & 미구매고객
def create_url_and_non_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                    purchase_event_name="Purchase", contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 and 전환완료 고객
def create_specific_page_and_coversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 conversion_event_name="ViewContent", contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        ], "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 and 미 전환 고객
def create_url_and_non_coversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                     conversion_event_name="ViewContent", contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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


# URL포함 and 회원가입 고객
def create_specific_page_and_registration_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                    registration_event_name="CompleteRegistration", contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

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
                        ], "retention_seconds": 15552000,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": ""
                                },
                                {
                                    "operator": "or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template": "VISITORS_BY_URL"
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
