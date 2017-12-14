from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# 특정페이지 방문 ( NEO 타겟, UTM 타겟 등 기능 동일)
def create_specific_page_visitor_customers(account_id, name, pixel_id, retention_days=30, prefill=True,
                                           contain_list=[]):
    try:
        ad_account = AdAccount(fbid=account_id)

        filters = []
        for str in contain_list:
            filters.append({
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
                        "filter":
                            {
                                "operator": "and",
                                "filters": [
                                    {
                                        "field": "url",
                                        "operator": "i_contains",
                                        "value": ""
                                    }, {
                                        "operator": "or",
                                        "filters": filters
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
