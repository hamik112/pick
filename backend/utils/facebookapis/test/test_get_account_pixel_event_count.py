from facebookads.exceptions import FacebookRequestError
# from django.conf import settings

from facebookads import FacebookAdsApi
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adspixel import AdsPixel

SYSTEM_USER_TOKEN = 'EAAUsxsN1snQBAHss8zEYNWpegIrZCLiOzZASUoAAyR177teuCatcjFdTRHSZBKrsRz06tAGVDpmra3UEwjaRwxxg0QCJ7qDyOpGzt5G4z7wTnDDctQZCFSlNcLf5222gRJsKkEscRgv6tkIggAiV8zY9jmhQSpAWYkMWmEqSUwZDZD'
FACEBOOK_APP_ID = 1456607077970548
FACEBOOK_APP_SECRET = 'e74075b09b2854a21a32c79cdad67c60'

try:
    FacebookAdsApi.init(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, SYSTEM_USER_TOKEN)

    account_id = 'act_894360037304328'

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
            "locale":"ko_KR"
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
                else :
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

        # return return_pixel_events
        print(return_pixel_events)

except FacebookRequestError as e:
    print(e)
    msg = {}
    msg['request_context'] = e._request_context
    msg['error'] = e._error
    raise Exception(msg)