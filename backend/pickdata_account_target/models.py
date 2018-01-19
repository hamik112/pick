from django.db import models
from utils.common import string_formatter

from fb_ad_account.models import FbAdAccount

import traceback
import logging

logger = logging.getLogger(__name__)


class PickdataAccountTarget(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)

    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', db_constraint=False, null=False)
    target_audience_id = models.BigIntegerField()

    pixel_mapping_category = models.ForeignKey('pixel_mapping_category.PixelMappingCategory',
                                               db_constraint=False,
                                               null=False)
    target_status = models.IntegerField()
    description = models.TextField()  # View에 표시하기 위한 용도?

    def get_list(self, fb_ad_account_id=None):
        try:
            if fb_ad_account_id != None:
                fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

                pickdata_account_targets = self.objects.filter(fb_ad_account=fb_ad_account)
            else:
                pickdata_account_targets = self.objects.all()

            return pickdata_account_targets

        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    def create(self, fb_ad_account, target_audience_id, pixel_mapping_category, description, target_status=0, username="TEST"):
        try:
            created_account_target = PickdataAccountTarget()

            created_account_target.updated_by = username
            created_account_target.updated_by = username

            created_account_target.fb_ad_account = fb_ad_account
            created_account_target.target_audience_id = target_audience_id

            created_account_target.pixel_mapping_category = pixel_mapping_category
            created_account_target.target_status = target_status
            created_account_target.description = description

            created_account_target.save()

            return created_account_target
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    def check_by_description(self, fb_ad_account, pixel_mapping_category, description_str):
        try:
            result = True

            try:
                pickdata_account_target = self.objects.get(fb_ad_account=fb_ad_account,
                                                           pixel_mapping_category=pixel_mapping_category,
                                                           description=description_str)
                result = False
            except self.DoesNotExist:
                description = string_formatter.string_to_literal(description_str)

                pickdata_account_targets = self.objects.filter(fb_ad_account=fb_ad_account,
                                                               pixel_mapping_category=pixel_mapping_category)
                for pickdata_account_target in pickdata_account_targets:
                    if description == string_formatter.string_to_literal(pickdata_account_target.description):
                        result = False
                        break
            return result

        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return True

    class Meta:
        db_table = "pickdata_account_targets"
