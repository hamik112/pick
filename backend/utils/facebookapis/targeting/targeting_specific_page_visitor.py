from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 특정페이지 전체 방문자
def create_specific_page_total_visitor_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 contain_list=[], eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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

def update_specific_page_total_visitor_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                 contain_list=[], eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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


# 특정페이지 방문자 & 이용시간 상위 고객
def create_usage_time_top_customers(account_id, name, pixel_id, prefill=True, retention_days=30, input_percent=25,
                                    contain_list=[], eq_list=[]):
    try:
        input_percent = int(input_percent)
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        max_percent = 100
        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
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
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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

def update_usage_time_top_customers(custom_audience_id, name, pixel_id, prefill=True, retention_days=30, input_percent=25,
                                    contain_list=[], eq_list=[]):
    try:
        input_percent = int(input_percent)
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        max_percent = 100
        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
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
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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


# 특정페이지방문 & 특정일 동안 미방문 고객
def create_non_visition_customers(account_id, name, pixel_id, prefill=True, retention_days=30, exclusion_retention_days=1, contain_list=[],
                                  eq_list=[]):
    try:

        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        rules_exclusions = []
        contain_rule_exclusions = {}
        eq_rule_exclusions = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        if (len(contain_filters) > 0):
            contain_rule_exclusions = {
                "event_sources": [
                    {
                        "type": "pixel",
                        "id": pixel_id
                    }
                ],
                "retention_seconds": exclusion_retention_days * 24 * 60 * 60,
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
            rules_exclusions.append(contain_rule_exclusions)

        if (len(eq_filter) > 0):
            eq_rule_exclusions = {
                "event_sources": [
                    {
                        "type": "pixel",
                        "id": pixel_id
                    }
                ],
                "retention_seconds": exclusion_retention_days * 24 * 60 * 60,
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules_exclusions.append(eq_rule_exclusions)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
            },
            "exclusions": {
                "operator": "or",
                "rules": rules_exclusions
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

def update_non_visition_customers(custom_audience_id, name, pixel_id, prefill=True, retention_days=30, exclusion_retention_days=1, contain_list=[],
                                  eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        rules_exclusions = []
        contain_rule_exclusions = {}
        eq_rule_exclusions = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        if (len(contain_filters) > 0):
            contain_rule_exclusions = {
                "event_sources": [
                    {
                        "type": "pixel",
                        "id": pixel_id
                    }
                ],
                "retention_seconds": exclusion_retention_days * 24 * 60 * 60,
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
            rules_exclusions.append(contain_rule_exclusions)

        if (len(eq_filter) > 0):
            eq_rule_exclusions = {
                "event_sources": [
                    {
                        "type": "pixel",
                        "id": pixel_id
                    }
                ],
                "retention_seconds": exclusion_retention_days * 24 * 60 * 60,
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules_exclusions.append(eq_rule_exclusions)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
            },
            "exclusions": {
                "operator": "or",
                "rules": rules_exclusions
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


# 특정페이지방문 and 장바구니 고객
def create_specific_page_and_addtocart_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 addtocart_evnet_name="AddToCart", contain_list=[], eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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
                            # ], "retention_seconds": retention_days * 24 * 60 * 60,
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

def update_specific_page_and_addtocart_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                 addtocart_evnet_name="AddToCart", contain_list=[], eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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
                            # ], "retention_seconds": retention_days * 24 * 60 * 60,
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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


# 특정페이지 방문 & 구매고객
def create_specific_page_and_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                purchase_event_name="Purchase", contain_list=[], eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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

def update_specific_page_and_purchase_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                purchase_event_name="Purchase", contain_list=[], eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 특정페이지방문 & 미구매고객
def create_specific_page_and_non_purchase_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                    purchase_event_name="Purchase", contain_list=[], eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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

def update_specific_page_and_non_purchase_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                    purchase_event_name="Purchase", contain_list=[], eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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


# 특정페이지방문 and 전환완료 고객
def create_specific_page_and_coversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                 conversion_event_name="ViewContent", contain_list=[], eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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

def update_specific_page_and_coversion_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                 conversion_event_name="ViewContent", contain_list=[], eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


# 특정페이지방문 and 미 전환 고객
def create_specific_page_and_non_coversion_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                     conversion_event_name="ViewContent", contain_list=[], eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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

def update_specific_page_and_non_coversion_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                     conversion_event_name="ViewContent", contain_list=[], eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        eq_filter = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": value
            })

        rule = {}
        rules = []
        contain_rule = {}
        eq_rule = {}
        if (len(contain_filters) > 0):
            contain_rule = {
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
            rules.append(contain_rule)

        if (len(eq_filter) > 0):
            eq_rule = {
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
                            "filters": eq_filter
                        }
                    ]
                },
                "template": "VISITORS_BY_URL"
            }
            rules.append(eq_rule)

        rule = {
            "inclusions": {
                "operator": "or",
                "rules": rules
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


# 특정페이지방문 and 회원가입 고객
def create_specific_page_and_registration_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                                    registration_event_name="CompleteRegistration", contain_list=[],
                                                    eq_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        contain_filters = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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

def update_specific_page_and_registration_customers(custom_audience_id, name, pixel_id, retention_days=30, prefill=True,
                                                    registration_event_name="CompleteRegistration", contain_list=[],
                                                    eq_list=[]):
    try:
        custom_audience = CustomAudience(custom_audience_id)

        contain_filters = []
        for value in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
            })

        for value in eq_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": value
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

        audience = custom_audience.remote_update(params=params)

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
