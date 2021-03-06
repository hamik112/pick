from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError
from utils.common import convert_list

# 사이트방문 전체 고객
def get_custom_audience(audience_id):
    try:
        custom_audience = CustomAudience(audience_id)

        return_audience = custom_audience.remote_read(fields=[
            CustomAudience.Field.id,
            CustomAudience.Field.name,
            CustomAudience.Field.account_id,
            CustomAudience.Field.approximate_count,
            CustomAudience.Field.delivery_status,
            CustomAudience.Field.operation_status,
            CustomAudience.Field.pixel_id,
            CustomAudience.Field.time_created,
            CustomAudience.Field.time_updated
        ])

        return_audience = return_audience._json

        return return_audience

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def get_custom_audience_by_ids(audience_ids):
    try:
        splited_list = convert_list.split_list(audience_ids)
        return_data = []

        for splited_ids in splited_list:

            custom_audience = CustomAudience()
            custom_audiences = custom_audience.get_by_ids(splited_ids, fields=[
                CustomAudience.Field.id,
                CustomAudience.Field.name,
                CustomAudience.Field.account_id,
                CustomAudience.Field.approximate_count,
                CustomAudience.Field.delivery_status,
                CustomAudience.Field.operation_status,
                CustomAudience.Field.pixel_id,
                CustomAudience.Field.time_created,
                CustomAudience.Field.time_updated
            ])

            data = [custom_audience._json for custom_audience in custom_audiences]
            return_data = return_data + data

        return return_data

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)


def get_dic_custom_audiences_by_ids(audience_ids):
    try:
        if audience_ids != []:
            return_data = {}
            splited_list = convert_list.split_list(audience_ids)

            for splited_ids in splited_list:
                custom_audience = CustomAudience()
                custom_audiences = custom_audience.get_by_ids(splited_ids, fields=[
                    CustomAudience.Field.id,
                    CustomAudience.Field.name,
                    CustomAudience.Field.account_id,
                    CustomAudience.Field.approximate_count,
                    CustomAudience.Field.delivery_status,
                    CustomAudience.Field.operation_status,
                    CustomAudience.Field.pixel_id,
                    CustomAudience.Field.time_created,
                    CustomAudience.Field.time_updated
                ], params={
                    'locale': 'ko_KR'
                })

                data = {custom_audience.get('id'): custom_audience._json for custom_audience in custom_audiences}
                return_data.update(data)

            return return_data
        else:
            return None

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
