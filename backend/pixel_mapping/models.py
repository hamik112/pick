from django.db import models
from pixel_mapping_category.models import PixelMappingCategory
from pixel_mapping_category.serializers import PixelMappingCategorySerializer
from utils.common.string_formatter import string_to_literal

import traceback
import logging
import json

logger = logging.getLogger(__name__)

class PixelMapping(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', db_constraint=False, null=False)
    facebook_pixel_event_name = models.CharField(max_length=128, null=True)
    pixel_mapping_category = models.ForeignKey('pixel_mapping_category.PixelMappingCategory', db_constraint=False, null=False)

    def get_pixel_mapping_by_id(self, pixel_mapping_id):
        try:
            pixel_mapping = PixelMapping.objects.get(pk=pixel_mapping_id)

            return pixel_mapping
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return None

    def get_list_by_fb_ad_account_id(self, fb_ad_account_id=0):
        if fb_ad_account_id == 0:
            return None
        try:
            pixel_mappings = self.objects.filter(fb_ad_account_id=fb_ad_account_id)

            # return_data = []
            #
            # for pixel_mapping in pixel_mappings:
            #     return_data.append({
            #         "fb_ad_account_id" : pixel_mapping.fb_ad_account_id,
            #         "pixel_mapping_category_id" : pixel_mapping.pixel_mapping_category_id,
            #         "facebook_pixel_event_name": pixel_mapping.facebook_pixel_event_name
            #     })

            # PixelMappingSerializer

            return pixel_mappings
        except self.DoesNotExist:
            return None
        except Exception as e:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            # TODO return []
            return None

    def create_or_update(self, fb_ad_account, facebook_pixel_event_names = [], pixel_mapping_category_ids = [], username = 'Test'):
        created_cnt = 0

        fb_ad_account_id = fb_ad_account.id

        for idx, pixel_mapping_category_id in enumerate(pixel_mapping_category_ids):
            if facebook_pixel_event_names[idx] != None:
                try:
                    pixel_mapping = self.objects.get(fb_ad_account_id = fb_ad_account_id ,pixel_mapping_category_id=pixel_mapping_category_id)

                    pixel_mapping.updated_by = username
                    pixel_mapping.fb_ad_account = fb_ad_account
                    pixel_mapping.pixel_mapping_category_id = pixel_mapping_category_id
                    pixel_mapping.facebook_pixel_event_name = facebook_pixel_event_names[idx]

                except self.DoesNotExist:
                    pixel_mapping = PixelMapping()

                    pixel_mapping.created_by = username
                    pixel_mapping.updated_by = username
                    pixel_mapping.fb_ad_account = fb_ad_account
                    pixel_mapping.pixel_mapping_category_id = pixel_mapping_category_id
                    pixel_mapping.facebook_pixel_event_name = facebook_pixel_event_names[idx]

                pixel_mapping.save()
                created_cnt += 1


        self.objects.exclude(pixel_mapping_category_id__in = pixel_mapping_category_ids).delete()
        return created_cnt

    class Meta:
        db_table = "pixel_mappings"
        unique_together = ("fb_ad_account", "facebook_pixel_event_name", "pixel_mapping_category")