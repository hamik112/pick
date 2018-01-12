from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adspixel import AdsPixel
from facebookads.adobjects.adspixelstats import AdsPixelStats
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError


# GET Account Default pixel 이벤트 리스트
def get_account_pixel_events(account_id):
    try:
        ad_account = AdAccount(fbid=account_id)

        ads_pixels = ad_account.get_ads_pixels(fields=[
            AdsPixel.Field.id,
            AdsPixel.Field.name,
            AdsPixel.Field.code,
            AdsPixel.Field.owner_ad_account
        ])

        account_pixel = None

        for ad_pixel in ads_pixels:
            account_id = ad_pixel.get(AdsPixel.Field.owner_ad_account).get('account_id')
            account_pixel = ad_pixel._json

        return_pixel_events = []
        if account_pixel != None:
            pixel_events = {}

            print(account_pixel)
            pixel_id = account_pixel.get('id')

            pixel = AdsPixel(pixel_id)

            stats_params = {
                "aggregation": "event",
                "start_time": "-30 days",
                "locale": "ko_KR"
            }
            event_stats = pixel.get_stats(params=stats_params)

            # print(event_stats)

            for event_data in event_stats:
                data_list = event_data.get('data')
                timestamp = event_data.get('timestamp')

                for data in data_list:
                    val = data.get('value')
                    cnt = data.get('count')

                    if pixel_events.get(val, None) == None:
                        pixel_events[val] = {
                            "count": cnt,
                            "timestamp": timestamp
                        }
                    else:
                        before_val = pixel_events[val].get('count')
                        pixel_events[val] = {
                            "count": before_val + cnt,
                            "timestamp": timestamp
                        }

            print(pixel_events)
            for pixel_event_key in pixel_events:
                return_pixel_events.append({
                    "name":pixel_event_key,
                    "count":pixel_events[pixel_event_key].get('count'),
                    "timestamp":pixel_events[pixel_event_key].get('timestamp')
                })

        return return_pixel_events

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)

# GET Account Default pixel
def get_account_default_pixel(account_id):
    try:
        # print("get_account_default_pixel")
        ad_account = AdAccount(fbid=account_id)

        ads_pixels = ad_account.get_ads_pixels(fields=[
            AdsPixel.Field.id,
            AdsPixel.Field.name,
            AdsPixel.Field.code,
            AdsPixel.Field.owner_ad_account
        ])

        # print("ads_pixels : ", ads_pixels)
        account_pixel = None

        for ad_pixel in ads_pixels:
            account_id = ad_pixel.get(AdsPixel.Field.owner_ad_account).get('account_id')
            account_pixel = ad_pixel._json

        return account_pixel

    except FacebookRequestError as e:
        print(e)
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)