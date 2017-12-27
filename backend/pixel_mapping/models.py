from django.db import models

class PixelMapping(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', db_constraint=False, null=False)
    facebook_pixel_event_name = models.CharField(max_length=128)
    pixel_mapping_category = models.ForeignKey('pixel_mapping_category.PixelMappingCategory', db_constraint=False, null=False)

    class Meta:
        db_table = "pixel_mappings"