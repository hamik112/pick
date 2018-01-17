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
        for str in contain_list:
            contain_filters.append({
                "field": "url",
                "operator": "i_contains",
                "value": str
            })

        for str in eq_list:
            eq_filter.append({
                "field": "url",
                "operator": "eq",
                "value": str
            })

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
                                    "value":""
                                },{
                                    "operator":"or",
                                    "filters": contain_filters
                                }
                            ]
                        },
                        "template":"VISITORS_BY_URL"
                    },{
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
                                    "value":""
                                },{
                                    "operator":"or",
                                    "filters":eq_filter
                                }
                            ]
                        },
                        "template":"VISITORS_BY_URL"
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





        rule = {
            "inclusions":{
                "operator":"or",
                "rules":[
                    {
                        "event_sources":[
                            {
                                "type":"pixel",
                                "id":"515448565280358"
                            }
                        ],
                        "retention_seconds":2592000,
                        "filter":{
                            "operator":"and",
                            "filters":[
                                {
                                    "field":"url",
                                    "operator":"i_contains",
                                    "value":""
                                },{
                                    "operator":"or",
                                    "filters":[
                                        {
                                            "field":"url",
                                            "operator":"i_contains",
                                            "value":"a"
                                        },{
                                            "field":"url",
                                            "operator":"i_contains",
                                            "value":"b"
                                        },{
                                            "field":"url",
                                            "operator":"i_contains",
                                            "value":"c"
                                        },{
                                            "field":"url",
                                            "operator":"i_contains",
                                            "value":"d"
                                        }
                                    ]
                                }
                            ]
                        },
                        "template":"VISITORS_BY_URL"
                    },{
                        "event_sources":[
                            {
                                "type":"pixel",
                                "id":"515448565280358"
                            }
                        ],
                        "retention_seconds":2592000,
                        "filter":{
                            "operator":"and",
                            "filters":[
                                {
                                    "field":"url",
                                    "operator":"i_contains",
                                    "value":""
                                },{
                                    "operator":"or",
                                    "filters":[
                                        {
                                            "field":"url",
                                            "operator":"eq",
                                            "value":"e"
                                        },{
                                            "field":"url",
                                            "operator":"eq",
                                            "value":"f"
                                        },{
                                            "field":"url",
                                            "operator":"eq",
                                            "value":"g"
                                        },{
                                            "field":"url",
                                            "operator":"eq",
                                            "value":"h"
                                        }
                                    ]
                                }
                            ]
                        },
                        "template":"VISITORS_BY_URL"
                    }
                ]
            },
            "exclusions":{
                "operator":"or",
                "rules":[
                    {
                        "event_sources":[
                            {
                                "type":"pixel",
                                "id":"515448565280358"
                            }
                        ],
                        "retention_seconds":2592000,
                        "filter":{
                            "operator":"and",
                            "filters":[
                                {
                                    "field":"event",
                                    "operator":"eq",
                                    "value":"PageView"
                                }
                            ]
                        }
                    }
                ]
            }
        }