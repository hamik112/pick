from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError

# 사이트방문 전체고객 and 구매고객
def create_visitor_and_purchase_customers(account_id, pixel_id='', name='', retention_days=15):
    try:
        pass

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 사이트방문 전체고객 and 미구매고객
def create_visitor_and_non_purchase_customers(account_id):
    try:
        pass
        # 전체고객 - 구매고객
    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 구매고객 전체
def create_purchase_customers(account_id, pixel_id='', name='', retention_days=15):
    try:
        pass
        ad_account = AdAccount(fbid=account_id)
        audience = ad_account.create_custom_audience(params={
            CustomAudience.Field.name: name,
            CustomAudience.Field.pixel_id: pixel_id,
            CustomAudience.Field.subtype: CustomAudience.Subtype.website,
            CustomAudience.Field.retention_days: retention_days,
            CustomAudience.Field.rule: {
                "and": [
                    {
                        "event": {
                            "i_contatins": "purchase"
                        }
                    }
                ]
            }
        })

        return audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 특정 구매횟수 이상 구매 고객
def create_more_than_x_timtes_purchase_customers(account_id, purchase_count = 0 ):
    try:
        pass

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 특정 구매금액 이상 구매 고객
def create_more_than_x_amount_purchjase_customers(account_id, purchase_amount = 0 ):
    try:
        pass

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# 장바구니 고객중 미구매 고객

# 회원가입 고객중 미구매 고객

