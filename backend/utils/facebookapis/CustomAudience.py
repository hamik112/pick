from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.exceptions import FacebookRequestError

import pprint
import logging
import traceback

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


def create_lookalike_audience(ad_account_id):
    try:
        ad_account = AdAccount(fbid=ad_account_id)

        params = {
            CustomAudience.Field.name: 'My lookalike audience',
            CustomAudience.Field.subtype: CustomAudience.Subtype.lookalike,
            CustomAudience.Field.origin_audience_id: '<SEED_AUDIENCE_ID>',
            CustomAudience.Field.lookalike_spec: {
                'type': 'similarity',
                'country': 'US',
            },
        }
        lookalike = ad_account.create_custom_audience(params=params)

        return lookalike

    except FacebookRequestError as e:
        logger.error(traceback.format_exc())
        msg = {}
        msg['request_context'] = e._request_context
        msg['error'] = e._error
        raise Exception(msg)
